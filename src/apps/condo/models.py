import uuid

from brutils import format_cnpj, remove_symbols_cnpj
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django_countries.fields import CountryField


# Base Class
class DateLogsBaseModel(models.Model):
    """
    Every model must have:
    - uuid as id
    - created_at attribute
    - updated_at attribute
    So this is a base class created in order to keep DRY practices.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # If abstract=True, django will NOT create the table in db.
        abstract = True


class Condominium(DateLogsBaseModel):
    name = models.CharField(max_length=120, blank=False, null=False, unique=True)
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        blank=False,
        null=False,
    )
    address1 = models.CharField(max_length=150)
    address2 = models.CharField(max_length=150, default="")
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=30)
    country = CountryField()
    postal_code = models.CharField(max_length=20)
    description = models.TextField(help_text="Write details about your condominium.")
    cover = models.ImageField(upload_to="condo_me/condominiums/%Y/%m/%d/", blank=True)

    def __str__(self) -> str:
        return self.name

    def num_of_blocks(self) -> int:
        return self.blocks.count()

    def num_of_apartments(self) -> int:
        apartments_qty = 0
        for block in self.blocks.all():
            apartments_qty += block.get_apartments_count()
        return apartments_qty

    def clean_cnpj(self):
        """
        Validates and formats the CNPJ field specifically.
        """
        # Remove symbols from cnpj data
        cnpj_no_symbols = remove_symbols_cnpj(self.cnpj)

        # validate ('None" if invalid) and format cnpj
        formatted_cnpj = format_cnpj(cnpj_no_symbols)
        if formatted_cnpj is None:
            raise ValidationError(
                "Please, insert a 14 digits valid CNPJ, with or without symbols."
            )
        return formatted_cnpj

    def clean(self):
        """
        This method orchestrates all validation rules and is called during full_clean().
        """
        super().clean()
        try:
            self.cnpj = self.clean_cnpj()
        except ValidationError as e:
            raise ValidationError({"cnpj": e.message})

    def save(self, *args, **kwargs):
        """
        Ensures validation happens before saving.
        This guarantees that no invalid data can be saved to the database.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        app_label = "condo"


class Block(DateLogsBaseModel):
    name = models.CharField(
        max_length=120,
        default="Main Block",
        blank=False,
        null=False,
    )
    description = models.TextField(
        help_text="Write details about this block.", null=True, blank=True
    )
    condominium = models.ForeignKey(
        to=Condominium,
        on_delete=models.CASCADE,
        related_name="blocks",
        blank=False,
        null=False,
    )
    cover = models.ImageField(
        upload_to="condo_me/blocks/%Y/%m/%d/",
        blank=True,
        null=True,
        verbose_name="Cover Image",
        help_text="Upload an image for this block",
    )

    def __str__(self) -> str:
        return self.name

    def get_cover_url(self):
        """Returns the URL of the cover image or a default image
        if none exists
        """
        if self.cover and hasattr(self.cover, "url"):
            return self.cover.url
        return None

    def get_apartments_count(self):
        return self.apartments.count()

    class Meta:
        app_label = "condo"
        # Lots of condominiums may have 'Block A', but a specific condominium may have
        # only one. So:
        unique_together = ["name", "condominium"]


class Apartment(DateLogsBaseModel):
    number_or_name = models.CharField(max_length=20, verbose_name="Number (or name)")
    block = models.ForeignKey(
        to=Block, on_delete=models.CASCADE, related_name="apartments"
    )
    condominium = models.ForeignKey(
        to=Condominium, on_delete=models.CASCADE, related_name="apartments"
    )

    class Meta:
        ordering = ["number_or_name", "block"]
        app_label = "condo"

    def __str__(self) -> str:
        return f"{self.number_or_name}{self.block}"

    def num_of_residents(self):
        return self.residents.count()

    def get_residents(self):
        names = [
            f"{resident.first_name} {resident.last_name}"
            for resident in self.residents.all()
        ]
        return ", ".join(names)


class CommonArea(DateLogsBaseModel):
    MINIMUM_USING_MINUTES = [(30, "30"), (60, "60")]

    name = models.CharField(max_length=50)
    condominium = models.ForeignKey(
        to=Condominium, on_delete=models.CASCADE, related_name="common_areas"
    )
    description = models.TextField(
        help_text="Write details and rules about this Common Area."
    )
    opens_at = models.TimeField(auto_now=False, blank=False)
    closes_at = models.TimeField(auto_now=False, blank=False)
    whole_day = models.BooleanField(verbose_name="Must be a whole day reservation?")
    paid_area = models.BooleanField(verbose_name="User have to pay for use?")
    price = models.DecimalField(
        "Price",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="In Brazilian Reais",
    )
    minimum_using_minutes = models.IntegerField(
        "Minimum using time in minutes",
        choices=MINIMUM_USING_MINUTES,
        blank=True,
        null=True,
        help_text="Leave blank in case of whole day use.",
    )
    maximum_using_fraction = models.IntegerField(
        verbose_name="Choose an integer. It will be multiplied by minimum \
            using minutes (above) in order to obtain maximum using time \
                (bellow)",
        blank=True,
        null=True,
        help_text="Leave blank in case of whole day use.",
    )

    # this field will be automaticaly calculated on __init__
    maximum_using_time = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Maximum using time (minutes)",
        help_text="It will be blank in case of whole day use.",
    )
    cover = models.ImageField(upload_to="common_areas/%Y/%m/%d/", blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    def calc_maximum_usage(self):
        if self.minimum_using_minutes and self.maximum_using_fraction:
            return self.minimum_using_minutes * self.maximum_using_fraction

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.maximum_using_time = self.calc_maximum_usage()

    def clean(self):
        if self.whole_day and self.maximum_using_time:
            raise ValidationError(
                "No need to choose maximum minutes of use per day in case \
                    of whole day reservation"
            )
        elif self.paid_area and not self.price:
            raise ValidationError(
                "You confirmed this is a paid common area.Please inform usage \
                    price."
            )
        elif not self.paid_area and self.price:
            raise ValidationError(
                "You confirmed this is NOT a paid common area. Please remove \
                    its usage price."
            )
        elif self.whole_day and (
            self.minimum_using_minutes or self.maximum_using_fraction
        ):
            raise ValidationError(
                "If whole day reservation is selected, maximum minutes of \
                    use and/or maximum using fraction should not be \
                        specified."
            )

    class Meta:
        app_label = "condo"


class SetupProgress(DateLogsBaseModel):
    """
    Tracks the setup progress of a condominium in the system in order to
    give reference to a manager user.
    Each step is represented by a boolean field indicating if that
    configuration has been completed.
    """

    condominium = models.OneToOneField(
        "Condominium", on_delete=models.CASCADE, related_name="setup_progress"
    )
    has_condominium = models.BooleanField(default=False)
    has_blocks = models.BooleanField(default=False)
    has_apartments = models.BooleanField(default=False)
    has_common_areas = models.BooleanField(default=False)
    has_residents = models.BooleanField(default=False)

    @property
    def setup_percentage(self):
        """Calculates the completion percentage of the condominium setup"""
        total_steps = 5
        completed_steps = sum(
            [
                self.has_condominium,
                self.has_blocks,
                self.has_apartments,
                self.has_common_areas,
                self.has_residents,
            ]
        )
        return (completed_steps / total_steps) * 100

    @property
    def next_step(self):
        """Returns the next step that needs to be configured. Order matters."""
        if not self.has_condominium:
            return "Create your condominium"
        if not self.has_blocks:
            return "Create at least one block"
        if not self.has_apartments:
            return "Add apartments to block"
        if not self.has_residents:
            return "Send invitation to residents join the system"
        if not self.has_common_areas:
            return "Create a common area"
        return "Condominium Setup Complete"

    def update_status(self):
        """
        Updates the condominium setup status based on existing relatioships
        """
        self.has_condominium = (
            get_user_model().objects.filter(condominium=self.condominium).exists()
        )
        self.has_blocks = self.condominium.blocks.exists()
        self.has_apartments = any(
            block.apartments.exists() for block in self.condominium.blocks.all()
        )
        self.has_residents = self.condominium.condo_person.filter(
            groups__name="resident"
        ).exists()
        self.has_common_areas = self.condominium.common_areas.exists()
        self.save()
