from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from SportskiKlub.utils import get_all_coaches_from_db, get_all_locations_from_db, create_group, update_group, delete_group, get_all_terms_from_db
from SportskiKlub.serializers import CoachSerializer, LocationSerializer, GroupPostSerializer, GroupResponsePostSerializer, TermSerializer, GroupUpdateSerializer

class CoachesView(APIView):
    def get(self, request):
        coaches = get_all_coaches_from_db()
        locations = get_all_locations_from_db()
        terms = get_all_terms_from_db()
        serializerCoach = CoachSerializer(coaches, many=True)
        serializerLocation = LocationSerializer(locations, many=True)
        serializerTerm = TermSerializer(terms, many=True)
        return Response({"coaches": serializerCoach.data, "locations": serializerLocation.data, "terms": serializerTerm.data}, status=status.HTTP_200_OK)

class GroupView(APIView):
    def post(self, request):
        serializerPost = GroupPostSerializer(data=request.data)
        if serializerPost.is_valid():
            response = create_group(request.data['coachId'], request.data['termId'], request.data['locationId'], request.data['name'])
            if response != None:
                serializerResponse = GroupResponsePostSerializer({"groupId": str(response)})
                return Response(serializerResponse.data, status=status.HTTP_201_CREATED)

        return Response(serializerPost.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupChangesView(APIView):
    def put(self, request, id):
        serializerPut = GroupUpdateSerializer(data=request.data)
        if serializerPut.is_valid():
            if update_group(id, serializerPut.data['termId'], serializerPut.data['locationId'], serializerPut.data['name']):
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        if delete_group(id):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


