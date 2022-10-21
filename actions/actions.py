# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from email import message
from typing import Any, Text, Dict, List
from unittest import result
from urllib import response
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from sqlalchemy import false
from swiplserver import PrologMQI, PrologThread
import random
import os.path
import json
import time
import random

# Archivos Json

class OperarArchivosJson():

    # Archivo Opiniones
    
    @staticmethod
    def cargarArchivoOpiniones(): 
        if os.path.isfile(".\\actions\\opiniones.json"):
            with open(".\\actions\\opiniones.json","r") as archivo_carga:
                retorno=json.load(archivo_carga)
                archivo_carga.close()
        else:
            retorno={}
        return retorno

    # Archivo Porque
    
    @staticmethod
    def cargarArchivoPorque(): 
        if os.path.isfile(".\\actions\\porque.json"):
            with open(".\\actions\\porque.json","r") as archivo_carga:
                retorno=json.load(archivo_carga)
                archivo_carga.close()
        else:
            retorno={}
        return retorno
    
    # Arquivo Personas
    
    @staticmethod
    def guardarPersona(AGuardar):
        with open(".\\actions\\personas.json","w") as archivo_descarga:
            json.dump(AGuardar, archivo_descarga, indent=4)
        archivo_descarga.close()

    @staticmethod
    def cargarArchivoPersona(): 
        if os.path.isfile(".\\actions\\personas.json"):
            with open(".\\actions\\personas.json","r") as archivo_carga:
                retorno=json.load(archivo_carga)
                archivo_carga.close()
        else:
            retorno={}
        return retorno
    
    @staticmethod
    def cargarArchivoResoluciones(): 
        if os.path.isfile(".\\actions\\resoluciones.json"):
            with open(".\\actions\\resoluciones.json","r") as archivo_carga:
                retorno=json.load(archivo_carga)
                archivo_carga.close()
        else:
            retorno={}
        return retorno
    


class ActionMateriasCursando(Action):

    def name(self) -> Text:
        return "action_cursando"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query_async(r"consult('C:\\Users\\s7tan\\OneDrive\\Desktop\\Universidad\\Programacion Exploratoria\\Prolog\\PlanDeEstudio.pl')", find_all=False)
                prolog_thread.query_async(f"materias_que_curso(X)", find_all=False)
                result = prolog_thread.query_async_result()[0]['X']
                message='Estoy Cursando: \n'
                for materia in result:
                    message=message+materia+'\n'
                dispatcher.utter_message(text=f"{message}")
        return[]

class ActionOpinionMaterias(Action):
    
    def name(self) -> Text:
        return "action_opinionMaterias"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        materia = next(tracker.get_latest_entity_values("materias"), None)
        print(materia)
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query_async(r"consult('C:\\Users\\s7tan\\OneDrive\\Desktop\\Universidad\\Programacion Exploratoria\\Prolog\\PlanDeEstudio.pl')", find_all=False)
                prolog_thread.query_async(f"materia_en_cursada('{materia}')", find_all=False)
                materiasEnCursada = prolog_thread.query_async_result()
                prolog_thread.query_async(f"materia_sin_cursar('{materia}')", find_all=False)
                materiasSinCursar = prolog_thread.query_async_result()
                if materiasEnCursada:
                    message='La estoy cursando, mas a adelante te digo'
                elif materiasSinCursar:
                    message='No te puedo decir, la curso mas adelante'
                else:
                    opiniones = OperarArchivosJson.cargarArchivoOpiniones()
                    if materia in opiniones:
                        message=opiniones[materia]['opinion']
                    else:
                        message='No te puedo responder, no tengo una opinion formada'
                dispatcher.utter_message(text=str(message))
        return []
    
class ActionMateriasAprobadas(Action):
        
    def name(self) -> Text:
       return "action_materiasAprobadas"
        
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query_async(r"consult('C:\\Users\\s7tan\\OneDrive\\Desktop\\Universidad\\Programacion Exploratoria\\Prolog\\PlanDeEstudio.pl')", find_all=False)
                prolog_thread.query_async(f"materias_aprobadas(X)", find_all=False)
                result = prolog_thread.query_async_result()[0]['X']
                message='Aprobe estas materias: \n'
                for materia in result:
                    message=message+materia+'\n'
                dispatcher.utter_message(text=f"{message}")
            return[] 
        
class ActionPorque(Action):
    
    def name(self) -> Text:
       return "action_porque"
   
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        opiniones = OperarArchivosJson.cargarArchivoPorque()
        consulta = tracker.get_slot('porque')
        print(consulta)
        message='No me lo he puesto a pensar'
        print('pase')
        if str(consulta) in opiniones:
            message=opiniones[consulta]['porque']
        dispatcher.utter_message(text=str(message))
        return []

class ActionEstadoMateria(Action):
    
    def name(self) -> Text:
        return "action_estadoMateria"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        materia = next(tracker.get_latest_entity_values("materias"), None)
        print(materia)
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query_async(r"consult('C:\\Users\\s7tan\\OneDrive\\Desktop\\Universidad\\Programacion Exploratoria\\Prolog\\PlanDeEstudio.pl')", find_all=False)
                prolog_thread.query_async(f"materia_aprobada('{materia}')", find_all=False)
                result=prolog_thread.query_async_result()
                if result:
                    dispatcher.utter_message(response="utter_aprobada")
                else:
                    prolog_thread.query_async(f"materia_en_cursada('{materia}')", find_all=False)
                    result=prolog_thread.query_async_result()
                    if result:
                        dispatcher.utter_message(response="utter_cursado")
                    else:
                        dispatcher.utter_message(response="utter_aunNoAprobada")
                        return [SlotSet('porque', "noAprobada")]
        return []

class ActionExtraerDatos(Action):
    
    def name(self) -> Text:
       return "action_extraer_datos"
   
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        personas = OperarArchivosJson.cargarArchivoPersona()
        dni = next(tracker.get_latest_entity_values('nro_dni'), None)
        print('entre')
        if str(dni) in personas:
            dispatcher.utter_message(text=str('Hola de nuevo ' + personas[dni]['nombre']))
            dispatcher.utter_message(response="utter_consultaComoesta")
            time.sleep(1)
            consulProfe=str(personas[dni]['esProfesor'])
            return [SlotSet('esProfesor',consulProfe)]
        else:
            dispatcher.utter_message(text=str('No te tenia agendado, ahi te agrego!'))
            time.sleep(1)
            dispatcher.utter_message(response="utter_consultaComoesta")
            return []

class ActionCargarSiEsProfesor(Action):
        
    def name(self) -> Text:
        return "action_cargarProfesor"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        datoProfesor = tracker.get_slot('esProfesor')
        dni = tracker.get_slot('dni')
        nombre = tracker.get_slot('nombre')
        personas = OperarArchivosJson.cargarArchivoPersona()
        personas[dni]={}
        personas[dni]['nombre']=str(nombre)
        personas[dni]['esProfesor']=str(datoProfesor)
        OperarArchivosJson.guardarPersona(personas)
        return []
    
class ActionDobleResponse(Action):
    
    def name(self) -> Text:
        return "action_DobleResponse"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('pase')
        dispatcher.utter_message(response="utter_devolucionEstadoAnimo")
        time.sleep(1)
        print('pase')
        dispatcher.utter_message(response="utter_consultarSiesProfesor")
        print('pase')
        return[]
    
class ActionConsultaCarrera(Action):
    
    def name(self) -> Text:
        return "action_consultaCarrera"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        consulta = tracker.get_slot('temaCarrera')
        print(consulta)
        if consulta:
            intent = tracker.get_intent_of_latest_message()
            if str(intent) == "consultaCarrera":
                dispatcher.utter_message(response="utter_consultaCarrera")
            else:
                dispatcher.utter_message(response="utter_dondeEstudio")
            return[SlotSet('temaCarrera',False)]
        elif str(tracker.get_intent_of_latest_message()) == "dondeEstudio":
            dispatcher.utter_message(response="utter_dondeEstudio")
        else:
            valor = random.randint(-1,1)
            print(valor)
            if (valor >= 0):
                dispatcher.utter_message(text="Bien, esta siendo un buen dia")
                return [SlotSet('porque',"buenDia")]
            else:
                dispatcher.utter_message(text="Mas o menos, es un dia complicado")
                return [SlotSet('porque',"malDia")]
            

                

# Grupal

class Action_consultar_por_ejercicio(Action): # 
    def name(self) -> Text:
        return "action_consultar_por_ejercicio"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("la materia por entidad es: " + str(next(tracker.get_latest_entity_values("materias"), None)))
        print("el tp de la materia es:" + str(next(tracker.get_latest_entity_values("tp"), None)))
        print("el inciso de la materia es:" + str(next(tracker.get_latest_entity_values("inciso"), None)))
        tp = next(tracker.get_latest_entity_values("tp"), None)
        inciso = next(tracker.get_latest_entity_values("tp"), None)
        if (next(tracker.get_latest_entity_values("materias"), None) != None):
            materia = next(tracker.get_latest_entity_values("materias"), None)
        else:
            materia = None
        if (materia != None):
            try:
                datos = OperarArchivosJson.cargarArchivoResoluciones()
                materiaLower = datos["tranformacionesDeNombresMaterias"][materia.lower()]
                ejercicio = datos["ejercicios"][materiaLower][tp][inciso]
                print(materiaLower)
                print(ejercicio)
                dispatcher.utter_message(response="utter_paso_el_ejercicio")
            except:
                dispatcher.utter_message(response="utter_no_tengo_ejercicio")#, tp=tp,inciso=inciso, materia=materia)
        else:
            dispatcher.utter_message(response="utter_no_conozco_materia")
        return []