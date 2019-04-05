async def test_context_models(context):
    assert context.models.test
    o = await context.models.test.objects.create(id=1)
    assert o
    o = await context.models.test.get_by_id(1)
    assert o
    o = await context.models.test.get_by_id_sql(1)
    assert o


async def test_orm(context):
    from .models import Test
    d = await Test.objects.all()
    assert d
