# Generated by Django 4.2.7 on 2025-04-15 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0019_alter_c2bpaymentsconfirmation_msisdn_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardPaymentsTransactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('req_locale', models.CharField(max_length=10)),
                ('req_payer_authentication_indicator', models.CharField(max_length=5)),
                ('payer_authentication_acs_transaction_id', models.CharField(max_length=100)),
                ('req_card_type_selection_indicator', models.CharField(max_length=5)),
                ('auth_trans_ref_no', models.CharField(max_length=50)),
                ('payer_authentication_enroll_veres_enrolled', models.CharField(max_length=5)),
                ('req_bill_to_surname', models.CharField(max_length=100)),
                ('req_card_expiry_date', models.CharField(max_length=10)),
                ('merchant_advice_code', models.CharField(max_length=10)),
                ('req_bill_to_phone', models.CharField(max_length=20)),
                ('card_type_name', models.CharField(max_length=50)),
                ('auth_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('auth_response', models.CharField(max_length=5)),
                ('bill_trans_ref_no', models.CharField(max_length=50)),
                ('req_payment_method', models.CharField(max_length=20)),
                ('req_payer_authentication_merchant_name', models.CharField(max_length=100)),
                ('auth_time', models.DateTimeField()),
                ('transaction_id', models.CharField(max_length=50)),
                ('req_card_type', models.CharField(max_length=10)),
                ('payer_authentication_transaction_id', models.CharField(max_length=100)),
                ('payer_authentication_pares_status', models.CharField(max_length=5)),
                ('payer_authentication_cavv', models.CharField(max_length=255)),
                ('auth_avs_code', models.CharField(max_length=5)),
                ('auth_code', models.CharField(max_length=20)),
                ('payment_token_instrument_identifier_new', models.CharField(max_length=5)),
                ('payer_authentication_specification_version', models.CharField(max_length=10)),
                ('req_bill_to_address_country', models.CharField(max_length=5)),
                ('req_profile_id', models.CharField(max_length=100)),
                ('signed_date_time', models.DateTimeField()),
                ('req_bill_to_address_line1', models.CharField(max_length=255)),
                ('payer_authentication_validate_e_commerce_indicator', models.CharField(max_length=10)),
                ('req_card_number', models.CharField(max_length=30)),
                ('signature', models.TextField()),
                ('payment_token', models.CharField(max_length=100)),
                ('payment_token_instrument_identifier_id', models.CharField(max_length=50)),
                ('req_bill_to_address_city', models.CharField(max_length=100)),
                ('auth_cavv_result', models.CharField(max_length=5)),
                ('reason_code', models.CharField(max_length=10)),
                ('req_bill_to_forename', models.CharField(max_length=100)),
                ('req_payer_authentication_acs_window_size', models.CharField(max_length=5)),
                ('payment_account_reference', models.CharField(max_length=100)),
                ('request_token', models.TextField()),
                ('req_device_fingerprint_id', models.CharField(max_length=100)),
                ('auth_cavv_result_raw', models.CharField(max_length=5)),
                ('req_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('req_bill_to_email', models.EmailField(max_length=254)),
                ('payer_authentication_reason_code', models.CharField(max_length=10)),
                ('auth_avs_code_raw', models.CharField(max_length=5)),
                ('req_currency', models.CharField(max_length=5)),
                ('decision', models.CharField(max_length=20)),
                ('message', models.TextField()),
                ('req_transaction_uuid', models.CharField(max_length=50)),
                ('payer_authentication_eci', models.CharField(max_length=5)),
                ('req_transaction_type', models.CharField(max_length=100)),
                ('payer_authentication_xid', models.CharField(max_length=255)),
                ('req_access_key', models.CharField(max_length=50)),
                ('req_reference_number', models.CharField(max_length=50)),
                ('payer_authentication_validate_result', models.CharField(max_length=10)),
                ('payment_token_instrument_identifier_status', models.CharField(max_length=20)),
                ('auth_reconciliation_reference_number', models.CharField(max_length=100)),
                ('signed_field_names', models.TextField()),
                ('send_sms', models.BooleanField(default=False)),
                ('p_flag', models.PositiveBigIntegerField(default=0)),
                ('imarika_flag', models.BooleanField(default=False)),
                ('igas_flag', models.BooleanField(default=False)),
                ('sirius_status', models.BooleanField(default=False)),
                ('intergration_status', models.CharField(blank=True, max_length=255, null=True)),
                ('integration_date', models.DateTimeField(blank=True, null=True)),
                ('sirius_error_description', models.TextField(blank=True, null=True)),
                ('user_id', models.CharField(blank=True, max_length=255, null=True)),
                ('user_name', models.CharField(blank=True, max_length=255, null=True)),
                ('is_from_reconcilliation', models.BooleanField(default=False)),
                ('fetch_id', models.CharField(blank=True, max_length=255, null=True)),
                ('group_id', models.CharField(blank=True, max_length=255, null=True)),
                ('pollkava', models.CharField(blank=True, max_length=255, null=True)),
                ('kavaflag', models.CharField(blank=True, max_length=255, null=True)),
                ('kavaresult', models.TextField(blank=True, null=True)),
                ('p_kava', models.CharField(blank=True, max_length=255, null=True)),
                ('p_kava_result', models.TextField(blank=True, null=True)),
                ('fa_updated_date', models.DateTimeField(blank=True, null=True)),
                ('lob_policyNumber', models.CharField(blank=True, max_length=255, null=True)),
                ('recon_comment', models.TextField(blank=True, null=True)),
                ('is_valid_trans', models.BooleanField(default=False)),
                ('p_aims', models.TextField(blank=True, null=True)),
                ('aims_result', models.CharField(blank=True, max_length=255, null=True)),
                ('cellulant_flag', models.CharField(blank=True, max_length=255, null=True)),
                ('column2', models.TextField(blank=True, null=True)),
                ('newappflag', models.BooleanField(default=False)),
                ('confirmation_status', models.BooleanField(default=False)),
                ('company_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payments.company')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
