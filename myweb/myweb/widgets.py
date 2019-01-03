
from django.forms import widgets



def input_factor(describe,cls_name='form-control',**kwargs):
    widgets_tuple = widgets.__all__[3:]
    if describe in widgets_tuple:
        input_class = getattr(widgets,describe)
        obj = input_class(
                attrs={
                    'class':cls_name
                }
            )
        if kwargs:
            obj.attrs = dict(obj.attrs,**kwargs)
        return obj
    else:
        raise  AttributeError('widgets has no attribute named %s'%describe)
