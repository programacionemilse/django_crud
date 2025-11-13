from django import forms
from .models import Tarea

class crearTareaForm(forms.ModelForm):
    class Meta:
        #le indico el modelo del que se va a crear el formulario
        model = Tarea
        #le digo los campos que va a incluir el formulario (usar el nombre que llevan en el modelo los campos)
        fields = ['titulo','descripcion','importante']

        widgets = {
            'titulo': forms.TextInput(attrs= {'class':'form-control', 'placeholder':'Ingrese el titulo del proyecto'}),
            'descripcion': forms.Textarea(attrs= {'class':'form-control', 'placeholder':'Ingrese la descripción de proyecto'}),
            'importante': forms.CheckboxInput(attrs= {'class':'form-check-input m-auto','type':"checkbox"})
        }