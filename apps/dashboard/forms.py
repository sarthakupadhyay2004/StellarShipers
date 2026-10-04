import json
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from apps.rfq.models import RFQ
from apps.products.models import Product, Category
from apps.pages.models import FAQ
from apps.core.models import CompanyProfile, SocialLink

class DashboardLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:outline-none text-sm font-mono',
            'placeholder': 'Admin Username',
            'autocomplete': 'username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:outline-none text-sm font-mono',
            'placeholder': 'Password',
            'autocomplete': 'current-password',
        })
    )


class DashboardRFQStatusForm(forms.ModelForm):
    class Meta:
        model = RFQ
        fields = ['status', 'admin_notes']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'w-full px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-xs font-mono font-semibold focus:ring-2 focus:ring-blue-500 focus:outline-none',
            }),
            'admin_notes': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-xs font-mono focus:ring-2 focus:ring-blue-500 focus:outline-none',
                'rows': 5,
                'placeholder': 'Record mill allocations, freight quotes, negotiation logs, or follow-up notes...',
            }),
        }


class DashboardFAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['category', 'question', 'answer', 'display_order', 'is_active']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm font-mono focus:ring-2 focus:ring-blue-500 focus:outline-none',
            }),
            'question': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none',
                'placeholder': 'e.g. Do you charge for samples?',
            }),
            'answer': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none',
                'rows': 5,
                'placeholder': 'Provide clear, procurement-oriented B2B answer...',
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'w-32 px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm font-mono focus:ring-2 focus:ring-blue-500 focus:outline-none',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500',
            }),
        }


class DashboardProductForm(forms.ModelForm):
    applications_raw = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-xs font-mono focus:ring-2 focus:ring-blue-500 focus:outline-none',
            'rows': 4,
            'placeholder': 'Enter one application per line:\nNatural-fiber textile development\nBlended yarn development\nWoven or nonwoven material',
        }),
        help_text="One potential application per line."
    )

    class Meta:
        model = Product
        fields = [
            'name', 'category', 'tagline', 'description',
            'raw_material', 'extraction_method', 'processing', 'supplier_notes',
            'harvest_origin', 'moq', 'packaging_details', 'hs_code',
            'is_active', 'is_featured', 'display_order'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm focus:ring-2 focus:ring-blue-500'}),
            'category': forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm'}),
            'tagline': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm', 'rows': 4}),
            'raw_material': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm font-mono'}),
            'extraction_method': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm font-mono'}),
            'processing': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm font-mono'}),
            'supplier_notes': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-xs font-mono', 'rows': 2}),
            'harvest_origin': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm font-mono'}),
            'moq': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm font-mono'}),
            'packaging_details': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm font-mono'}),
            'hs_code': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm font-mono'}),
            'display_order': forms.NumberInput(attrs={'class': 'w-32 px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm font-mono'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if isinstance(self.instance.applications, list):
                self.fields['applications_raw'].initial = "\n".join(self.instance.applications)

    def save(self, commit=True):
        instance = super().save(commit=False)
        apps_text = self.cleaned_data.get('applications_raw', '')
        instance.applications = [line.strip() for line in apps_text.splitlines() if line.strip()]
        if commit:
            instance.save()
        return instance


class DashboardCompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = [
            'company_name', 'primary_email', 'primary_phone', 'address',
            'gstin', 'show_gstin', 'iec', 'show_iec', 'operational_scope'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm focus:ring-2 focus:ring-blue-500',
                'placeholder': 'STELLAR SHIPERS',
            }),
            'primary_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm font-mono focus:ring-2 focus:ring-blue-500',
                'placeholder': 'contact@stellarshipers.com',
            }),
            'primary_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm font-mono focus:ring-2 focus:ring-blue-500',
                'placeholder': '+91 98765 43210 / Available upon inquiry',
            }),
            'address': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm focus:ring-2 focus:ring-blue-500',
                'placeholder': 'India (or registered corporate office jurisdiction)',
            }),
            'gstin': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm font-mono tracking-wider uppercase focus:ring-2 focus:ring-blue-500',
                'placeholder': 'e.g. 07AAAAA0000A1Z5',
            }),
            'iec': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm font-mono tracking-wider uppercase focus:ring-2 focus:ring-blue-500',
                'placeholder': 'e.g. 0123456789',
            }),
            'show_gstin': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500',
            }),
            'show_iec': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500',
            }),
            'operational_scope': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-xs font-mono focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'B2B Maritime Cargo & Bulk Agro-Industrial Export Coordination...',
            }),
        }


class DashboardSocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ['platform', 'display_name', 'url', 'display_order', 'is_active']
        widgets = {
            'platform': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm font-mono focus:ring-2 focus:ring-blue-500',
            }),
            'display_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm focus:ring-2 focus:ring-blue-500',
                'placeholder': 'e.g. LinkedIn or Instagram',
            }),
            'url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm font-mono focus:ring-2 focus:ring-blue-500',
                'placeholder': 'https://linkedin.com/company/stellarshipers',
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'w-32 px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#161A1E] text-slate-900 dark:text-white text-sm font-mono focus:ring-2 focus:ring-blue-500',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500',
            }),
        }

