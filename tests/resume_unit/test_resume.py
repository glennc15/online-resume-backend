import json


def test_get_resume():
    with open("./events/event-get-resume.json", "r") as f:
        apigw_get_resume_event = json.load(f)


    from src.api import resume

    results = resume.resume_handler(apigw_get_resume_event, "")

    print(results)

