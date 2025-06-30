from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi import HTTPException
import requests
from datetime import datetime
from model.utils import predict


class inputData(BaseModel):
    """
    Input data model for the API.
    """
    feddit_name: str
    limit: Optional[int] = Field(
        default=5, ge=1, le=25, description="Number of comments to retrieve (1-25)")


class outputComment(BaseModel):
    """
    Model for individual comment output.
    """
    id: int
    text: str
    polarity: str
    polarity_score: float


class outputData(BaseModel):
    """
    Output data model for the API.
    Contains a list of comments with their polarity.
    """
    comments: list[outputComment] = Field(
        default_factory=list, description="List of comments with polarity")


class inputData_with_time(BaseModel):
    """
    Input data model for the API.
    """
    feddit_name: str
    time_range: List[datetime] = Field(...,
                                       description="Time range for filtering comments")


class outputComment_with_time(BaseModel):
    """
    Model for individual comment output.
    """
    id: int
    text: str
    polarity: str
    polarity_score: float
    created_at: datetime = Field(...,
                                 description="Creation time of the comment")


class outputData_with_time(BaseModel):
    """
    Output data model for the API.
    Contains a list of comments with their polarity.
    """
    comments_with_time: list[outputComment_with_time] = Field(
        default_factory=list, description="List of comments with polarity and creation time")


def sort_comments_by_polarity(comments: outputData) -> outputData:
    """
    Sorts comments by polarity.
    """
    # Implement sorting logic here
    sorted_comments = sorted(comments.comments, key=lambda x: x.polarity)
    return outputData(comments=sorted_comments)


def get_subfeddit_id(feddit_name: str) -> str:
    url = "http://localhost:8080/api/v1/subfeddits"

    payload = {"skip": 0,
               "limit": 10}
    response = requests.get(url, params=payload)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail="Error fetching subfeddits")

    response = response.json()

    for subfeddit in response['subfeddits']:
        if subfeddit['title'] == feddit_name:
            return subfeddit['id']
    raise ValueError(f"Subfeddit with name {feddit_name} not found")


def get_subfeddit_comments(subfeddit_id: str, limit: int = 5):
    url = "http://localhost:8080/api/v1/comments"

    payload = {"subfeddit_id": subfeddit_id,
               "skip": 0,
               "limit": limit}
    response = requests.get(url, params=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail="Error fetching comments")

    response = response.json()
    comments_list = response.get('comments', [])
    for comment in comments_list:
        predict_result = predict(comment["text"])
        comment["polarity"] = predict_result['label']
        comment["polarity_score"] = predict_result['confidence']
    return comments_list


def get_subfeddit_comments_with_time_range(subfeddit_id: str, time_range: List[datetime]):
    start, end = time_range
    if start >= end:
        raise ValueError("Start time must be strictly earlier than end time")

    url = "http://localhost:8080/api/v1/comments"
    limit = 1000
    skip = 0
    filtered_comments = []

    while True:
        response = requests.get(url, params={
            "subfeddit_id": subfeddit_id,
            "skip": skip,
            "limit": limit
        })

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code,
                                detail="Error fetching comments")

        comments_batch = response.json().get("comments", [])
        if not comments_batch:
            break

        for comment in comments_batch:
            comment_time = datetime.fromtimestamp(comment['created_at'])
            if comment_time < start:
                continue
            elif comment_time > end:
                return filtered_comments
            else:
                predict_result = predict(comment["text"])
                comment_with_polarity = {
                    **comment,
                    "created_at": comment_time,
                    "polarity": predict_result['label'],
                    "polarity_score": predict_result['confidence']
                }
                filtered_comments.append(comment_with_polarity)

        skip += limit

    return filtered_comments
