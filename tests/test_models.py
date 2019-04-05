async def test_orm(context):
    assert context.models.test
    await context.models.test.objects.create(id=1)
    o = await context.models.test.get_by_id(1)
    assert o
    o = await context.models.test.get_by_id_sql(1)
    assert o


async def test_model_class(context):
    from .models import Test
    d = await Test.objects.all()
    assert d
