from uuid import UUID

from app.authentication.domain.entities import RefreshTokenEntity
from app.authentication.domain.repositories import IRefreshTokenRepository
from app.authentication.infrastructure.models import RefreshToken


class RefreshTokenRepository(IRefreshTokenRepository):
    def save(self, entity: RefreshTokenEntity) -> RefreshTokenEntity:
        RefreshToken.objects.update_or_create(
            id=entity.id,
            defaults={
                'token': entity.token,
                'revoked': entity.revoked,
                'user_id': entity.user,
                'created_at': entity.created_at,
                'expire_at': entity.expire_at,
            },
        )

        return entity

    def find_by_hash(self, hash: str) -> RefreshTokenEntity | None:
        try:
            return self._to_model(RefreshToken.objects.get(token=hash))

        except RefreshToken.DoesNotExist:
            return None

    def revoke_all_by_user(self, user_id: UUID) -> None:
        RefreshToken.objects.filter(user=user_id).update(revoked=True)

    def _to_model(self, model: RefreshToken) -> RefreshTokenEntity:
        return RefreshTokenEntity(
            id=model.id,
            token=model.token,
            revoked=model.revoked,
            user=model.user.id,
            created_at=model.created_at,
            expire_at=model.expire_at,
        )
