from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer, ProjectSerializer
from .models import User, Project
from rest_framework.permissions import IsAuthenticated
import jwt, datetime
import csv
from sklearn.metrics.pairwise import cosine_similarity


# AI
from django.http import JsonResponse
from django.views import View
import pandas as pd
import numpy as np
from deep_translator import GoogleTranslator
from sklearn.metrics.pairwise import cosine_similarity
from rest_framework import status


# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        
        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            'id': user.id
        }
        return response

class CompleteUserView(APIView):
    def post(self, request):
        bio = request.POST.get('bio')
        id = request.POST.get('id')
        category = request.POST.get('category')

        user = User.objects.filter(id=int(id))
        if user.exists():
            u = user.first()
            u.bio = bio
            u.category = category
            u.id = id
            u.save()
            return Response({"bio": bio, "category": category, "id": id}, status=200)
        else:
            u = User()
            u.bio = bio
            u.category = category
            u.id = id  
            u.save()
            return Response({"bio": bio, "category": category, "id": id}, status=201)

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'secret', algorithm='HS256')
        except:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            user = User.objects.get(id=payload['id'])
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        
class UserExistsView(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            new_user_data = {
                'email': '',
                'password': '',
            }
            new_user_serializer = UserSerializer(data=new_user_data)
            if new_user_serializer.is_valid(raise_exception=True):
                new_user = new_user_serializer.save()
                return Response(new_user_serializer.data)
            

class CompleteUserView(APIView):
    def post(self, request):
        bio = request.POST.get('bio')
        category = request.POST.get('category')
        id = request.POST.get('id')
        user = User.objects.filter(id=id)
        if user.exists():
            u = user.first()
            u.bio = bio
            u.category = category
            u.save()

        else:
            u = User()
            u.bio = bio
            u.category = category
            u.id = id
            u.save()

        return Response({"id": id, "category": category, "bio": bio})

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
        
class ProjectView(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class populatedb(APIView):
    def get(self, request):
        with open('main/feed.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                project = Project(
                    project_id=row['project_id'],
                    project_name=row['project_name'], 
                    project_url_on_catalog=row['project_url_on_catalog'], 
                    project_url_external=row['project_url_external'], 
                    project_description=row['project_description'], 
                    keywords=row['keywords'], 
                    fields_of_science=row['fields_of_science'], 
                    project_status=row['project_status'], 
                    agency_sponsor=row['agency_sponsor'], 
                    agency_sponsor_other=row['agency_sponsor_other'], 
                    geographic_scope=row['geographic_scope'], 
                    participant_age=row['participant_age'], 
                    project_goals=row['project_goals'], 
                    participation_tasks=row['participation_tasks'], 
                    scistarter=row['scistarter'], 
                    email=row['email'], 
                    start_date=row['start_date']
                    )
                project.save()

class RecommendProjectsView(APIView):
    
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            description = user.bio

            if not description:
                return Response({"error": "No bio available for the user."})

            # Carregando csv pela url
            url = "https://www.citizenscience.gov/feed.csv"
            db = pd.read_csv(url)
            db['project_status'] = db['project_status'].str.lower()
            db['keywords'] = db['keywords'].str.lower()
            db = db[db['project_status'] == 'active']

            # Preprocessing description
            chars_to_remove = [",", "!", "?", ":", ".", "-", "_"]
            for char in chars_to_remove:
                description = description.replace(char, "")
            description_words = description.split(" ")
            description = ', '.join([GoogleTranslator(source='auto', target='en').translate(word) for word in description_words]).replace("\'", "")

            # Transformando coluna de ID para int e setando como índice
            db['project_id'] = pd.to_numeric(db['project_id']).astype('Int64')
            project_id = int(db['project_id'].iloc[-1]) + 1
            db = db[['project_id', 'keywords']].dropna()

            # Add description to db
            new_row = pd.DataFrame({'project_id': [project_id], 'keywords': [description]})
            db = pd.concat([db, new_row], ignore_index=True)

            
            # Generate tags
            clean_tags = db['keywords'].str.split(",")
            tag_columns = pd.get_dummies(clean_tags.apply(pd.Series).stack()).groupby(level=0).sum()
            all_tags = tag_columns.astype(bool).sum(axis=0).sort_values(ascending=False)
            tags = tag_columns[all_tags.index]

            # Compute similarities
            similarities = cosine_similarity(tags)
            db_similarity = pd.DataFrame(similarities, columns=db['project_id'], index=db['project_id']).reset_index()

            recommendations = db_similarity.nlargest(11, project_id)['project_id'].tolist()
            recommendations.remove(project_id)

            return Response({'recommendations': recommendations})

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)