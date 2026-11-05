"""Factory for creating fake Products for testing."""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Product, Category


class ProductFactory(factory.Factory):
    """Creates fake products."""

    class Meta:
        """Maps factory to the Product model."""
        model = Product

    id = factory.Sequence(lambda n: n)
    name = FuzzyChoice(choices=["Hat", "Shoes", "Big Mac", "Sheets", "Fedora"])
    description = factory.Faker("sentence")
    price = FuzzyChoice(choices=[10.50, 25.00, 59.95, 120.00])
    available = FuzzyChoice(choices=[True, False])
    category = FuzzyChoice(
        choices=[
            Category.UNKNOWN,
            Category.CLOTHS,
            Category.FOOD,
            Category.HOUSEWARES,
            Category.AUTOMOTIVE,
            Category.TOOLS,
        ]
    )
