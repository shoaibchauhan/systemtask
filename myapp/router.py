from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import ValidationError as PydanticValidationError
from django.core.exceptions import ObjectDoesNotExist
import pytz  # Proper exception handling for Django
from myapp.models import ProcessData
from myapp.schemas import ProcessDataRequest, ProcessDataResponse
from datetime import datetime
from django.utils import timezone as django_timezone

router = APIRouter()

from django.utils import timezone

@router.post("/api/process-data/")
def receive_process_data(request: ProcessDataRequest):
    try:
        # Iterate
        for process in request.processes:
            if not process.username:
                process.username = "Unknown"  

            if not process.name:
                process.name = "Unknown"  

            if isinstance(process.create_time, str):
                process.create_time = datetime.fromisoformat(process.create_time)

            # Make the datetime timezone-aware
            if timezone.is_naive(process.create_time):
                process.create_time = timezone.make_aware(process.create_time)

            if timezone.is_naive(request.timestamp):
                request.timestamp = timezone.make_aware(request.timestamp)

            # Saving
            ProcessData.objects.create(
                system_name=request.system_name,
                process_name=process.name,
                username=process.username,
                pid=process.pid,
                create_time=process.create_time,
                timestamp=request.timestamp,
            )

        return {"message": "Data successfully stored"}
    
    except PydanticValidationError as e:
        raise HTTPException(status_code=422, detail=f"Request validation error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")



@router.get("/api/all-process-by-system/", response_model=List[ProcessDataResponse])
def get_processes_by_system(system_name: str = Query(..., min_length=1)):
    try:
        processes = ProcessData.objects.filter(system_name=system_name)
        if not processes:
            raise HTTPException(status_code=404, detail=f"Processes not found for the system name: '{system_name}'")
        return processes
        
    except HTTPException as http_e:
        raise http_e
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.get("/api/process-by-time/")
def get_processes_by_time(
    start_time: datetime = Query(...), 
    end_time: datetime = Query(...),
):
    try:
        # Ensure start_time is earlier than end_time
        if start_time >= end_time:
            raise HTTPException(status_code=400, detail="start_time must be earlier than end_time")

        # Check if the datetime is aware (with timezone info)
        if start_time.tzinfo is None:
            start_time = pytz.utc.localize(start_time)  # Assuming UTC if no timezone is provided
        
        if end_time.tzinfo is None:
            end_time = pytz.utc.localize(end_time)  # Assuming UTC if no timezone is provided

        # Query the database for processes with create_time within the time range
        processes = ProcessData.objects.filter(create_time__gte=start_time, create_time__lte=end_time)
        
        if not processes.exists():
            raise HTTPException(status_code=404, detail="No processes found in the given time range")

        # Return the list of processes
        return [
            {
                "system_name": process.system_name,
                "process_name": process.process_name,
                "username": process.username,
                "pid": process.pid,
                "create_time": process.create_time,
                "timestamp": process.timestamp,
            }
            for process in processes
        ]
    except Exception as e:
        # Add more logging or error details to help troubleshoot
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    

@router.get("/api/process-duration/")
def get_process_duration(
    system_name: str = Query(..., min_length=1),
    process_name: str = Query(..., min_length=1),
):
    try:
        # Query the database for the process instances matching the system and process name
        process_instances = ProcessData.objects.filter(
            system_name=system_name, process_name=process_name
        )
        if not process_instances.exists():
            raise HTTPException(status_code=404, detail="Process not found")

        # Calculate the total duration in seconds for the process instances
        duration = sum(
            (process.timestamp - process.create_time).total_seconds()
            for process in process_instances
        )
        return {
            "system_name": system_name,
            "process_name": process_name,
            "duration": duration,
        }
    except ObjectDoesNotExist:
        raise HTTPException(status_code=404, detail="Process not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")