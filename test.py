from uuid import UUID

user_ids: list = [UUID('88fdb32f-d79d-4263-be2c-fb31a633492e')]
user_id: UUID = UUID('88fdb32f-d79d-4263-be2c-fb31a633492e')

print(user_id in user_ids)
