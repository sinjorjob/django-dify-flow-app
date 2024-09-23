from django.shortcuts import render
from django.http import JsonResponse
from .models import Category, Subcategory
import requests
import json
import time
from django.conf import settings

API_KEY = settings.API_KEY
BASE_URL = "https://api.dify.ai/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def index(request):
    categories = Category.objects.all()
    return render(request, 'dify_app/index.html', {'categories': categories})

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

def run_dify_workflow(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_inputs = {
            "category": data['category'],
            "subcategory": data['subcategory'],
            "details": data['details'],
            "query": data['query'],
        }
        user_id = "django_sysuser"

        result = run_workflow(user_inputs, user_id)
        if result:
            workflow_run_id, _ = result
            for _ in range(10):
                time.sleep(5)
                workflow_result = get_workflow_result(workflow_run_id)
                if workflow_result:
                    status = workflow_result.get('status')
                    if status == 'succeeded':
                        outputs = workflow_result.get('outputs')
                        if isinstance(outputs, str):
                            try:
                                outputs_dict = json.loads(outputs)
                                text_output = outputs_dict.get('text', '')
                            except json.JSONDecodeError:
                                text_output = outputs
                        elif isinstance(outputs, dict):
                            text_output = outputs.get('text', '')
                        else:
                            text_output = str(outputs)
                        return JsonResponse({'status': 'success', 'result': text_output})
                    elif status in ['failed', 'stopped']:
                        return JsonResponse({'status': 'error', 'message': f"ワークフローが{status}しました。"})
            return JsonResponse({'status': 'error', 'message': "ワークフローが予想時間内に完了しませんでした。"})
        else:
            return JsonResponse({'status': 'error', 'message': "ワークフローの開始に失敗しました。"})
    return JsonResponse({'status': 'error', 'message': "Invalid request method"})

def run_workflow(inputs, user_id):
    url = f"{BASE_URL}/workflows/run"
    payload = {
        "inputs": inputs,
        "response_mode": "blocking",
        "user": user_id
    }
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get('workflow_run_id'), result.get('task_id')
    except requests.RequestException:
        return None

def get_workflow_result(workflow_run_id):
    url = f"{BASE_URL}/workflows/run/{workflow_run_id}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None
