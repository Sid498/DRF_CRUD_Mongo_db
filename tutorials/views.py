from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from django.shortcuts import render
from rest_framework import status
from tutorials.models import Tutorial
from tutorials.serializers import TutorialSerializer
from rest_framework.decorators import api_view

@api_view(['GET', 'POST', 'DELETE'])
def tutorial_list(request):
    if request.method == "GET":
        tutorial = Tutorial.objects.all()

        tutorials_serializer = TutorialSerializer(tutorial, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
    elif request.method == "POST":
        # tutorial_data = JSONParser().parse(request.data)
        tutorials_serializer = TutorialSerializer(data=request.data)

        if tutorials_serializer.is_valid():
            tutorials_serializer.save()
            return JsonResponse(tutorials_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(tutorials_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        count = Tutorial.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were deleted'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'PUT', 'DELETE'])
def tutorial_detail(request, pk):
    try:
        tutorial = Tutorial.objects.get(id=pk)
    except Tutorial.DoesNotExist:
        return JsonResponse({'Error': 'Tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        tutorial_serializer = TutorialSerializer(tutorial)
        return JsonResponse(tutorial_serializer.data)
    elif request.method == "DELETE":
        tutorial.delete()
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    elif request.method == "PUT":
        tutorials_serializer = TutorialSerializer(tutorial, data=request.data)
        if tutorials_serializer.is_valid():
            tutorials_serializer.save()
            return JsonResponse(tutorials_serializer.data)
        else:
            return JsonResponse(tutorials_serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET'])
def tutorial_published(request):
    tutorial = Tutorial.objects.filter(published=True)
    tutorial_serializer = TutorialSerializer(tutorial, many=True)
    return JsonResponse(tutorial_serializer.data)
