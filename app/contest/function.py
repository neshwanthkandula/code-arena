from datetime import datetime, timedelta

def get_contest_state(start_time, duration_minutes):
    now = datetime.utcnow()
    end_time = start_time + timedelta(minutes=duration_minutes)

    if now<start_time:
        return "upcoming"
    elif start_time <= end_time:
        return "running"
    else:
        return "finished"
    
def get_problem_points(problem_index : int)->int:
    return problem_index*50