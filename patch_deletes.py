import os
import re

modules = {
    'bus_tracking': {
        'service': 'BusRouteService',
        'id_name': 'route_id',
        'get_method': 'get_by_id_and_school',
        'router_func': 'delete_bus_route',
        'router_var': 'route'
    },
    'cafeteria': {
        'service': 'MealPlanService',
        'id_name': 'plan_id',
        'get_method': 'get_by_id_and_school',
        'router_func': 'delete_meal_plan',
        'router_var': 'plan'
    },
    'custody': {
        'service': 'CustodyService',
        'id_name': 'order_id',
        'get_method': 'get_by_id',
        'router_func': 'delete_custody_order',
        'router_var': 'order'
    },
    'data_retention': {
        'service': 'RetentionPolicyService',
        'id_name': 'policy_id',
        'get_method': 'get_by_id',
        'router_func': 'delete_retention_policy',
        'router_var': 'policy'
    },
    'fundraising': {
        'service': 'CampaignService',
        'id_name': 'campaign_id',
        'get_method': 'get_by_id',
        'router_func': 'delete_campaign',
        'router_var': 'campaign'
    },
    'smc_reporting': {
        'service': 'SMCReportService',
        'id_name': 'report_id',
        'get_method': 'get_by_id',
        'router_func': 'delete_smc_report',
        'router_var': 'report'
    }
}

base_dir = 'apps/backend/src/edulafia/modules'

for mod, info in modules.items():
    svc_file = os.path.join(base_dir, mod, 'service.py')
    router_file = os.path.join(base_dir, mod, 'api/router.py')
    
    # 1. Update Service
    with open(svc_file, 'r') as f:
        svc_content = f.read()
    
    if 'async def delete(' not in svc_content:
        # Find the class
        class_regex = f"class {info['service']}:.*?(?=class |$)"
        match = re.search(class_regex, svc_content, re.DOTALL)
        if match:
            class_body = match.group(0)
            
            # Determine if get_method takes school_id
            if info['get_method'] == 'get_by_id_and_school':
                delete_method = f"""
    async def delete(self, {info['id_name']}: UUID, school_id: UUID) -> None:
        \"\"\"Delete a record.\"\"\"
        record = await self.repository.get_by_id_and_school({info['id_name']}, school_id)
        if not record:
            raise ValueError(f"Record not found")
        await self.repository.delete(record)
"""
            else:
                delete_method = f"""
    async def delete(self, {info['id_name']}: UUID) -> None:
        \"\"\"Delete a record.\"\"\"
        record = await self.repository.get_by_id({info['id_name']})
        if not record:
            raise ValueError(f"Record not found")
        await self.repository.delete(record)
"""
            
            new_class_body = class_body + delete_method
            svc_content = svc_content.replace(class_body, new_class_body)
            with open(svc_file, 'w') as f:
                f.write(svc_content)
            print(f"Updated {svc_file}")
            
    # 2. Update Router
    with open(router_file, 'r') as f:
        router_content = f.read()
        
    func_regex = f"async def {info['router_func']}.*?return {{\"message\": \".*?deleted\"}}"
    match = re.search(func_regex, router_content, re.DOTALL)
    if match:
        func_body = match.group(0)
        
        if 'await service.delete(' not in func_body:
            if info['get_method'] == 'get_by_id_and_school':
                delete_call = f"await service.delete({info['id_name']}, UUID(current_user['school_id']))"
            else:
                delete_call = f"await service.delete({info['id_name']})"
                
            new_func_body = func_body.replace('return {"message"', f'{delete_call}\n    return {{"message"')
            router_content = router_content.replace(func_body, new_func_body)
            with open(router_file, 'w') as f:
                f.write(router_content)
            print(f"Updated {router_file}")

