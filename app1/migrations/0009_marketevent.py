# Generated migration for MarketEvent model
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_users_cache'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text="Event headline (e.g., 'Tech Sector Rally on AI Breakthrough')", max_length=200)),
                ('description', models.TextField(help_text='Detailed description of the event and its market impact')),
                ('event_type', models.CharField(choices=[('sector_rally', 'Sector Rally'), ('sector_crash', 'Sector Crash'), ('sector_volatility', 'Sector Volatility'), ('market_news', 'Market News'), ('economic_data', 'Economic Data Release'), ('custom', 'Custom Event')], default='market_news', max_length=20)),
                ('affected_sector', models.CharField(blank=True, help_text='Sector affected (Technology, Healthcare, etc.)', max_length=50)),
                ('severity', models.CharField(choices=[('minor', 'Minor (±2%)'), ('moderate', 'Moderate (±5%)'), ('major', 'Major (±10%)'), ('extreme', 'Extreme (±15%)'), ('custom', 'Custom %')], default='moderate', max_length=10)),
                ('custom_percentage', models.DecimalField(blank=True, decimal_places=2, help_text='Custom percentage change (e.g., 7.50 for +7.5%)', max_digits=5, null=True)),
                ('is_positive', models.BooleanField(default=True, help_text='Is this a positive event (price increase)?')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('triggered_at', models.DateTimeField(blank=True, help_text='When the event was triggered', null=True)),
                ('scheduled_for', models.DateTimeField(blank=True, help_text='Schedule event for future time', null=True)),
                ('is_active', models.BooleanField(default=True, help_text='Show this event to teams?')),
                ('is_triggered', models.BooleanField(default=False, help_text='Has this event been triggered?')),
                ('stocks_affected', models.IntegerField(default=0, help_text='Number of stocks affected')),
                ('total_impact', models.TextField(blank=True, help_text='JSON data of price changes')),
            ],
            options={
                'verbose_name': 'Market Event',
                'verbose_name_plural': 'Market Events',
                'ordering': ['-created_at'],
            },
        ),
    ]
