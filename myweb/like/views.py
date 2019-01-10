from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import LikeCount,LikeRecord
# Create your views here.

def success_response(like_num):
	data = {}
	data['status'] = 'success'
	data['like_num'] = like_num
	return JsonResponse(data)

def erro_response(code, msg):
	data = {}
	data['status'] = 'Erro'
	data['code'] = code
	data['msg'] = msg
	return JsonResponse(data)

def like_change(req):
	user = req.user
	if not user.is_authenticated:
		return erro_response(400,'you have not login')
	content_type_name = req.GET.get('content_type')
	object_id = req.GET.get('object_id')
	is_like = req.GET.get('is_like')
	try:
		content_type = ContentType.objects.get(model=content_type_name)
		model_class = content_type.model_class()
		obje = model_class.objects.get(pk=object_id)
	except ObjectDoesNotExist:
		return erro_response(401,'object not exist')
	if is_like == 'true':
		#喜欢
		like_record, created = LikeRecord.objects.get_or_create(user=user,content_type=content_type,object_id=object_id)
		if created:
			#从未赞过,赞
			like_count ,created = LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
			like_count.count += 1
			like_count.save()
			return success_response(like_count.count) 
		else:
			return erro_response(400, '你已经赞过了')
	else:
		#取消赞
		if LikeRecord.objects.filter(user=user,content_type=content_type,object_id=object_id).exists():
			like_record = LikeRecord.objects.get(user=user,content_type=content_type,object_id=object_id)
			like_record.delete()
			like_count, created = LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
			if not created:
			#赞过
				like_count.count -= 1;
				like_count.save()
				return success_response(like_count.count) 
			else:
				return erro_response(404, 'data erro')
		else:
			return erro_response(401, '你没有赞过')
