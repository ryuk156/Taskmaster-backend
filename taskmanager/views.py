from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Board, Column, Card
from .serializers import BoardSerializer, ColumnSerializer, CardSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes


# Create your views here.
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_board(request):
    if request.method == 'POST':
        print(request.data)
        request.data['created_by'] = request.user.id
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_boards(request):
    if request.method == 'GET':
        boards = Board.objects.filter(created_by=request.user.id)
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_board(request, pk):
    if request.method == 'GET':
        board = Board.objects.get(pk=pk, created_by=request.user.id)
        serializer = BoardSerializer(board)
        return Response(serializer.data)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_board(request, pk):
    if request.method == 'DELETE':
        board = Board.objects.get(pk=pk, created_by=request.user.id)
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_board(request, pk):
    if request.method == 'PUT':
        board = Board.objects.get(pk=pk, created_by=request.user.id)
        serializer = BoardSerializer(board, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_column(request, board_id):
    try:
        board = Board.objects.get(pk=board_id, created_by=request.user.id)
    except Board.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        column_data = request.data.copy()
        column_data['board'] = board_id
        serializer = ColumnSerializer(data=column_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_columns(request):
    if request.method == 'GET':
        boards = Board.objects.filter(created_by=request.user)
        columns = Column.objects.filter(board__in=boards)
        serializer = ColumnSerializer(columns, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_column(request, pk):
    if request.method == 'GET':
        boards = Board.objects.filter(created_by=request.user)
        column = Column.objects.get(pk=pk, board__in=boards)
        serializer = ColumnSerializer(column)
        return Response(serializer.data)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_column(request, pk):
    if request.method == 'DELETE':
        column = Column.objects.get(pk=pk)
        column.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_column(request, pk):
    if request.method == 'PUT':
        column = Column.objects.get(pk=pk)
        serializer = ColumnSerializer(column, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_card(request, column_id):
    try:
        column = Column.objects.get(pk=column_id)
    except Column.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        board = column.board
        card_data = request.data.copy()
        card_data['column'] = column_id
        card_data['board'] = board
        serializer = CardSerializer(data=card_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_cards(request):
    if request.method == 'GET':
        cards = Card.objects.all()
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_card(request, pk):
    if request.method == 'GET':
        card = Card.objects.get(pk=pk)
        serializer = CardSerializer(card)
        return Response(serializer.data)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_card(request, pk):
    if request.method == 'DELETE':
        card = Card.objects.get(pk=pk)
        card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_card(request, pk):
    if request.method == 'PUT':
        try:
            card = Card.objects.get(pk=pk)
            column_id = request.data.get('column')
            if column_id is not None:
                column = Column.objects.get(pk=column_id)
                if card.column != column:
                    return Response({'message': 'Card does not belong to the specified column'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = CardSerializer(card, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Card.DoesNotExist:
            return Response({'message': 'Card does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Column.DoesNotExist:
            return Response({'message': 'Specified column does not exist'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def swap_card(request):
    if request.method == 'PUT':
        try:
            card1 = request.data.get('card_1')
            card2 = request.data.get('card_2')
            card1 = Card.objects.get(pk=card1)
            card2 = Card.objects.get(pk=card2)

            if card1.column != card2.column:
                return Response({'error': 'Cards do not belong to the same column'}, status=status.HTTP_400_BAD_REQUEST)
            card1.id, card2.id = card2.id, card1.id
            card1.save()
            card2.save()
            return Response({'message': 'Cards swapped successfully'}, status=status.HTTP_200_OK)
        except Card.DoesNotExist:
            return Response({"message": "One or both cards do not exist"}, status=status.HTTP_404_NOT_FOUND)

        
