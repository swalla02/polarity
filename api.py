from fastapi import FastAPI, HTTPException
from utils import (get_subfeddit_id,
                   get_subfeddit_comments,
                   get_subfeddit_comments_with_time_range,
                   inputData,
                   outputData,
                   outputComment,
                   inputData_with_time,
                   outputComment_with_time,
                   outputData_with_time)

app = FastAPI()


@app.post("/api/v1/comments_polarity/limit", response_model=outputData)
def get_comments_and_polarity_with_limit(input_data: inputData):
    """
    Endpoint to process the feddit name and return a response.
    """
    if not input_data.feddit_name:
        raise HTTPException(status_code=400, detail="feddit_name is required")

    try:
        subfeddit_id = get_subfeddit_id(input_data.feddit_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    try:
        comments = get_subfeddit_comments(subfeddit_id, input_data.limit)
    except HTTPException as e:
        raise e
    output = outputData(
        comments=[
            outputComment(
                id=comment['id'],
                text=comment['text'],
                polarity=comment['polarity'],
                polarity_score=comment['polarity_score']
            )
            for comment in comments
        ]
    )

    return output


@app.post("/api/v1/comments_polarity/with_time",
          response_model=outputData_with_time)
def get_comments_and_polarity_with_time_range(input_data: inputData_with_time):
    """
    Endpoint to process the feddit name, time range and return a response.
    """
    feddit_name = input_data.feddit_name
    time_range = input_data.time_range

    if not feddit_name:
        raise HTTPException(status_code=400, detail="feddit_name is required")

    try:
        subfeddit_id = get_subfeddit_id(feddit_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    try:
        comments_list = get_subfeddit_comments_with_time_range(
            subfeddit_id, time_range)
    except HTTPException as e:
        raise e
    output = outputData_with_time(
        comments_with_time=[
            outputComment_with_time(
                id=comment['id'],
                text=comment['text'],
                polarity=comment['polarity'],
                polarity_score=comment['polarity_score'],
                created_at=comment['created_at']
            )
            for comment in comments_list
            ]
        )

    return output
