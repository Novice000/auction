from .models import Listings, Bids, Comments
from django import forms
from .models import Bids

class ListingsForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ["title", "description","category","img_url","initial_bid"]
        widgets = {
            "title": forms.TextInput(attrs={"class":"form-control","placeholder":"title of listing"}),
            "description": forms.Textarea(attrs={"class":"form-control","placeholder":"write a description for your project"}),
            "category": forms.TextInput(attrs={"class":"form-control","placeholder":"category of listing e.g, Pet, Electronics, e.t.c"}),
            "img_url": forms.TextInput(attrs={"class":"form-control","placeholder":"put the image url for your listing"}),
            "initial_bid": forms.NumberInput(attrs={"class":"form-control", "placeholder":"Put the Initial bid here"}),
        }



class BidForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ["price"]
        widgets = {
            "price": forms.NumberInput(attrs={"class":"form-control"})
        }

    def __init__(self, *args, **kwargs):
        # Get the minimum value for bidding, passed as "highest_bid" in kwargs
        min_bid = kwargs.pop("highest_bid", None)
        super().__init__(*args, **kwargs)
        
        # Set the minimum value for "price" field dynamically
        if min_bid is not None:
            self.fields["price"].min_value = min_bid
            self.fields["price"].widget.attrs.update({
                "min": min_bid,    
                "step": "0.01"
            })


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ["comment"]
        widgets: {
            "comment": forms.Textarea(attrs={"class":"forms-control","style:":"height:40px"})
        }