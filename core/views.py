from django.http import JsonResponse
import json

from rest_framework.views import APIView

from core.serializers import UploadImageSerializer
from core.models import UploadImage
from core.mask_detect import mask_detection, np_encoder


class DetectMaskView(APIView):
    queryset = UploadImage.objects.all()
    serializer_class = UploadImageSerializer

    def post(self, request):
        img = request.data['img']
        result = mask_detection(img)
        print(result)

        return JsonResponse({'result': json.dumps(result, default=np_encoder)}, status=200)
