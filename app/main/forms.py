from django import forms


class CreateNewPackage(forms.Form):
    package_name = forms.CharField(required=True)
    sender_email = forms.EmailField(required=True)
    receiver_email = forms.EmailField(required=True)

    origin_latitude = forms.FloatField(required=True)
    origin_longitude = forms.FloatField(required=True)

    destination_latitude = forms.FloatField(required=True)
    destination_longitude = forms.FloatField(required=True)


class PassPackageID(forms.Form):
    package_id = forms.CharField(required=True)