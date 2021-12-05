from django.http import JsonResponse
import json
from threading import Thread

from rest_framework import viewsets
from rest_framework.views import APIView

from core.serializers import UploadImageSerializer, LogSerializer
from core.models import UploadImage, Log
from core.mask_detect import mask_detection, np_encoder
from core.adafruit_utils import open_door


class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer


def excute_detect_mask_tasks(masked, un_masked):
    # Saving log file
    new_log = Log(masked_user=len(masked), un_masked_user=len(un_masked))
    new_log.save()

    # open door when masked detected
    relay_data = 1 if len(masked) > 0 else 0
    open_door(relay_data)


class DetectMaskView(APIView):
    queryset = UploadImage.objects.all()
    serializer_class = UploadImageSerializer

    def post(self, request):
        img = request.data['img']
        result = mask_detection(img)

        masked = [face for face in result if face['label'] == 1]
        un_masked = [face for face in result if face['label'] == 0]

        print(result, masked, un_masked)

        # Excute task in other thread
        task = Thread(target=excute_detect_mask_tasks,
                      args=(masked, un_masked))
        task.start()

        return JsonResponse({'result': json.dumps(result, default=np_encoder)}, status=200)
