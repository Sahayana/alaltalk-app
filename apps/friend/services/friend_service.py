import random
from typing import List

from django.db import IntegrityError, transaction
from django.db.models import Q
from django.utils import timezone

from apps.account.models import CustomUser, UserLikeKeyWord
from apps.friend import constants
from apps.friend.helpers import W2V
from apps.friend.models import Friend, FriendRequest


class FriendService:
    @classmethod
    def send_friend_request(cls, user_id: int, target_user_id: int) -> FriendRequest:
        """
        친구 요청을 전송합니다.
        """
        try:
            friend_request = FriendRequest.objects.create(
                user_id=user_id,
                target_user_id=target_user_id,
                user_requested_at=timezone.now(),
            )
        except IntegrityError:
            raise IntegrityError("이미 존재하는 요청입니다.")

        return friend_request

    @classmethod
    @transaction.atomic
    def accept_friend_request(cls, target_user_id: int, request_id: int) -> Friend:
        """
        user의 친구 요청을 targetUser가 승낙하고 Friend 레코드를 생성합니다.
        """
        friend_request = FriendRequest.objects.select_related(
            "user", "target_user"
        ).get(id=request_id)

        if friend_request.target_user.id == target_user_id:
            try:
                friend = Friend.objects.create(
                    user_id=friend_request.user.id,
                    target_user_id=friend_request.target_user.id,
                )

                friend_request.user.friends.add(friend.target_user.id)
                friend_request.target_user.friends.add(friend.user.id)

                friend_request.status = constants.FriendRequestStatus.ACCEPT
                friend_request.targetuser_accept_at = timezone.now()
                friend_request.save()
            except IntegrityError:
                raise IntegrityError("이미 친구인 상태입니다.")
            return friend

    @classmethod
    def decline_friend_request(cls, target_user_id: int, request_id: int) -> None:
        """
        user의 친구 요청을 거절합니다.
        FriendRequest의 status를 DECLINE으로 변경합니다.
        """
        FriendRequest.objects.filter(
            id=request_id, target_user_id=target_user_id
        ).update(status=constants.FriendRequestStatus.DECLINE)

    @classmethod
    @transaction.atomic
    def disconnect_friend(cls, user_id: int, target_user_id: int) -> Friend:
        """
        친구 상태를 해제합니다.
        """
        friend_connections = Friend.objects.select_related(
            "user", "target_user"
        ).filter(
            Q(user_id=user_id, target_user_id=target_user_id)
            | Q(user_id=target_user_id, target_user_id=user_id)
        )
        friend_connections.update(status=constants.FriendStatus.DISCONNECTED)

        return friend_connections

    @classmethod
    def recommend_friend(cls, user: CustomUser) -> List[CustomUser]:
        """
        현재 친구가 아닌 유저들을 소개합니다.
        무작위 유저 100명을 선발하여, 키워드 유사도가 가장 높은 유저 5명을 추천합니다.
        """
        recommend_ratio = 5
        recommend_friends = []
        current_friend_ids = [friend.id for friend in user.friends.all()]
        strangers = (
            CustomUser.objects.exclude(id=user.id)
            .exclude(id__in=current_friend_ids)
            .order_by("?")
        )
        strangers_count = strangers.count()

        if strangers_count >= 100:
            strangers = strangers[:100]
        elif strangers_count < 6:
            strangers = strangers[: strangers_count - 1]
            recommend_friends = list(strangers)
            return recommend_friends
        else:
            strangers = strangers[: strangers_count - 1]

        user_keyword = UserLikeKeyWord.objects.filter(user_id=user.id).last()
        user_similarity_map = {}

        if not user_keyword or user_keyword == "":
            recommend_friends = random.sample(strangers, 5)
        else:
            for idx, stranger in enumerate(strangers):
                try:
                    simialrity = W2V.load().wv.similarity(
                        user_keyword, stranger.keyword
                    )
                    user_similarity_map[idx] = int(simialrity * 100)
                except Exception:
                    user_similarity_map[idx] = 0

            candidates = dict(
                sorted(user_similarity_map.items(), key=lambda x: x[1], reverse=True)[
                    :recommend_ratio
                ]
            )

            for candidate_idx in candidates.keys():
                recommend_friends.append(strangers[candidate_idx])

        return recommend_friends

    @classmethod
    def like_public_setting(cls, user_id: int, value: str) -> CustomUser:
        """
        유저의 좋아요 컨텐츠 노출을 ON/OFF 합니다.
        """

        if value == "ON":
            public_flag = True
        elif value == "OFF":
            public_flag = False

        user = CustomUser.objects.get(id=user_id)
        user.is_like_public = public_flag
        user.save()

        return user

    @classmethod
    def friend_like_recommend(cls, friend_id: int) -> List[str]:
        """
        채팅방에서 대화하는 친구의 관심 키워드를 '3개' 노출합니다.
        친구가 가진 키워드가 없으면 "찜 없음"을 반환하고, 갯수가 모자르면 유사도 모델을 통해 관심 키워드를 반환합니다.
        """
        recommend_ratio = 3
        friend_keywords = UserLikeKeyWord.objects.filter(user_id=friend_id).order_by(
            "-created_at"
        )[:recommend_ratio]
        keywords_count = friend_keywords.count()
        recommend_keywords = []

        if keywords_count == recommend_ratio:
            return [obj.keyword for obj in friend_keywords]
        elif keywords_count == 0:
            recommend_keywords.append("찜 없음")
        else:
            for word in friend_keywords:
                recommend_keywords.append(word.keyword)

            try:
                last_word = recommend_keywords[-1]
                similar_words = W2V.load().wv.most_similar(last_word)
                for word in similar_words[: recommend_ratio - len(recommend_keywords)]:
                    recommend_keywords.append(word)
            except Exception as e:
                raise e
        return recommend_keywords
