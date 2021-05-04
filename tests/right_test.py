from dataclasses import dataclass
import pytest
from main import _can_user_ping


@dataclass
class MockUser:
    id: int


@dataclass
class MockChatMember:
    user: MockUser
    status: str


@pytest.mark.parametrize("user_id,users,asrt",
                         [(1, ((1, "member"), (2, "creator")), None),
                          (2, ((1, "creator"), (2, "member")), None),
                          (1, ((1, "creator"), (2, "member")), True),
                          (1, ((1, "administrator"), (2, "member")), True),
                          ])
def test_can_user_ping(user_id, users, asrt):
    user = MockUser(user_id)
    users = [MockChatMember(MockUser(mu[0]), mu[1]) for mu in users]
    assert _can_user_ping(user, users) == asrt
