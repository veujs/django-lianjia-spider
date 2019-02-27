from django import forms

DISTRICT_CHOICES = (('yanta','雁塔'),('weiyang','未央'),('beilin','碑林'))
PRICE_CHOICES = (('p3','60-80万'),('p4','80-100万'),('p5','100-150万'))
BEDROOM_CHOICES = (('l2','两室'),('l3','三室'))


class HouseChoiceForm(forms.Form):
    district = forms.CharField(label='区域',widget=forms.RadioSelect(choices=DISTRICT_CHOICES))
    price = forms.CharField(label='价格',widget=forms.RadioSelect(choices=PRICE_CHOICES))
    bedroom = forms.CharField(label='庭室',widget=forms.RadioSelect(choices=BEDROOM_CHOICES))
    # district = forms.CharField(label='区域',widget=forms.RadioSelect(choices=DISTRICT_CHOICES))
    # price = forms.CharField(label='价格',widget=forms.RadioSelect(choices=PRICE_CHOICES))
    # bedroom = forms.CharField(label='庭室',widget=forms.RadioSelect(choices=BEDROOM_CHOICES))














