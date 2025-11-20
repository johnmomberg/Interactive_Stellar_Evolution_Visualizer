from dataclasses import dataclass 
from . import base_class 
from . import sub_stages 
from .. import file_paths 
from ... import misc 





################################################################################


@dataclass 
class MESA_model(base_class.BaseEntity): 
    mass: float 
    substage: sub_stages.SubStage 
    model_start: int 
    model_example: int 
    model_end: int 
    MESA_folder_path: str 

    # Automatically generate ID when object is created
    def __post_init__(self):
        self.id = f"Model(mass={self.mass}, model_example={self.model_example}, substage={self.substage})"


################################################################################


MODEL_0_2_NONE = MESA_model( 
    mass=0.2, 
    substage=sub_stages.SUB_NONE, 
    model_start=None, 
    model_example=None, 
    model_end=None, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=0.2")

MODEL_0_2_HAYASHI = MESA_model( 
    mass=0.2, 
    substage=sub_stages.SUB_HAYASHI, 
    model_start=1, 
    model_example=150, 
    model_end=225, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=0.2") 

MODEL_0_2_MS = MESA_model( 
    mass=0.2, 
    substage=sub_stages.SUB_MS_LOWMASS, 
    model_start=225, 
    model_example=273, 
    model_end=1000, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=0.2") 

MODEL_0_2_HEWD = MESA_model( 
    mass=0.2, 
    substage=sub_stages.SUB_WD_HE, 
    model_start=1000, 
    model_example=1200, 
    model_end=1224, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=0.2") 


################################################################################


MODEL_0_4_NONE = MESA_model( 
    mass=0.4, 
    substage=sub_stages.SUB_NONE, 
    model_start=None, 
    model_example=None, 
    model_end=None, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=0.4")

MODEL_0_4_HAYASHI = MESA_model( 
    mass=0.4, 
    substage=sub_stages.SUB_HAYASHI, 
    model_start=1, 
    model_example=200, 
    model_end=254, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=0.4") 

MODEL_0_4_MS = MESA_model( 
    mass=0.4, 
    substage=sub_stages.SUB_MS_MEDMASS, 
    model_start=254, 
    model_example=309, 
    model_end=350, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=0.4") 

MODEL_0_4_SUBGIANT = MESA_model( 
    mass=0.4, 
    substage=sub_stages.SUB_POSTMS_SUBGIANT, 
    model_start=350, 
    model_example=450, 
    model_end=1200, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=0.4") 

MODEL_0_4_RG = MESA_model( 
    mass=0.4, 
    substage=sub_stages.SUB_RG, 
    model_start=1200, 
    model_example=3000, 
    model_end=4850, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=0.4") 

MODEL_0_4_HEWD = MESA_model( 
    mass=0.4, 
    substage=sub_stages.SUB_WD_HE, 
    model_start=4850, 
    model_example=5159, 
    model_end=5159, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=0.4") 


################################################################################


MODEL_1_0_NONE = MESA_model( 
    mass=1.0, 
    substage=sub_stages.SUB_NONE, 
    model_start=None, 
    model_example=None, 
    model_end=None, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=1.0")

MODEL_1_0_HAYASHI = MESA_model( 
    mass=1.0, 
    substage=sub_stages.SUB_HAYASHI, 
    model_start=1,
    model_example=150, 
    model_end=202,
    MESA_folder_path=file_paths.MESA_data_folder/"M=1.0") 

MODEL_1_0_HENYEY = MESA_model( 
    mass=1.0, 
    substage=sub_stages.SUB_HENYEY, 
    model_start=202,
    model_example=220, 
    model_end=240,
    MESA_folder_path=file_paths.MESA_data_folder/"M=1.0") 

MODEL_1_0_MS = MESA_model( 
    mass=1.0, 
    substage=sub_stages.SUB_MS_MEDMASS, 
    model_start=240, 
    model_example=296, 
    model_end=330,
    MESA_folder_path=file_paths.MESA_data_folder/"M=1.0") 

MODEL_1_0_SUBGIANT = MESA_model( 
    mass=1.0, 
    substage=sub_stages.SUB_POSTMS_SUBGIANT, 
    model_start=330, 
    model_example=389, 
    model_end=415, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=1.0") 

MODEL_1_0_RG = MESA_model( 
    mass=1.0, 
    substage=sub_stages.SUB_RG, 
    model_start=415, 
    model_example=5000, 
    model_end=9500, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=1.0") 

MODEL_1_0_HEFLASH = MESA_model( 
    mass=1.0, 
    substage=sub_stages.SUB_HEIGN_HEFLASH, 
    model_start=9500, 
    model_example=9700, 
    model_end=10500, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=1.0") 

MODEL_1_0_HEMS = MESA_model( 
    mass=1.0, 
    substage=sub_stages.SUB_HEMS, 
    model_start=10500, 
    model_example=10650, 
    model_end=10950, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=1.0") 

MODEL_1_0_AGB = MESA_model(
    mass=1.0, 
    substage=sub_stages.SUB_AGB, 
    model_start=10950, 
    model_example=12300, 
    model_end=13600, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=1.0") 

MODEL_1_0_COWD = MESA_model( 
    mass=1.0, 
    substage=sub_stages.SUB_WD_CO, 
    model_start=13600, 
    model_example=14300, 
    model_end=14300, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=1.0") 


################################################################################


MODEL_1_75_NONE = MESA_model( 
    mass=1.75, 
    substage=sub_stages.SUB_NONE, 
    model_start=None, 
    model_example=None, 
    model_end=None, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=1.75")

MODEL_1_75_HAYASHI = MESA_model(
    mass=1.75, 
    substage=sub_stages.SUB_HAYASHI, 
    model_start=1, 
    model_example=140, 
    model_end=200, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=1.75")

MODEL_1_75_HENYEY = MESA_model(
    mass=1.75, 
    substage=sub_stages.SUB_HENYEY, 
    model_start=200, 
    model_example=235, 
    model_end=250, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=1.75")

MODEL_1_75_MS = MESA_model(
    mass=1.75, 
    substage=sub_stages.SUB_MS_HIMASS, 
    model_start=250, 
    model_example=285, 
    model_end=340, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=1.75")

MODEL_1_75_HGAP = MESA_model(
    mass=1.75, 
    substage=sub_stages.SUB_POSTMS_HGAP, 
    model_start=340, 
    model_example=389, 
    model_end=420, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=1.75")

MODEL_1_75_RG = MESA_model(
    mass=1.75, 
    substage=sub_stages.SUB_RG, 
    model_start=420, 
    model_example=1000, 
    model_end=8763, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=1.75")

MODEL_1_75_HEFLASH = MESA_model(
    mass=1.75, 
    substage=sub_stages.SUB_HEIGN_HEFLASH, 
    model_start=8763, 
    model_example=8802, 
    model_end=9000, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=1.75")

MODEL_1_75_HEMS = MESA_model(
    mass=1.75, 
    substage=sub_stages.SUB_HEMS, 
    model_start=9000, 
    model_example=9800, 
    model_end=10000, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=1.75")

MODEL_1_75_AGB = MESA_model(
    mass=1.75, 
    substage=sub_stages.SUB_AGB, 
    model_start=10000, 
    model_example=11425, 
    model_end=13635, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=1.75")

MODEL_1_75_COWD = MESA_model(
    mass=1.75, 
    substage=sub_stages.SUB_WD_CO, 
    model_start=13635, 
    model_example=None, 
    model_end=13635, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=1.75")


################################################################################


MODEL_3_0_NONE = MESA_model( 
    mass=3.0, 
    substage=sub_stages.SUB_NONE, 
    model_start=None, 
    model_example=None, 
    model_end=None, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=3.0")

MODEL_3_0_HAYASHI = MESA_model( 
    mass=3.0, 
    substage=sub_stages.SUB_HAYASHI, 
    model_start=1, 
    model_example=150, 
    model_end=195, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=3.0") 

MODEL_3_0_HENYEY = MESA_model( 
    mass=3.0, 
    substage=sub_stages.SUB_HENYEY, 
    model_start=195, 
    model_example=225, 
    model_end=250, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=3.0") 

MODEL_3_0_MS = MESA_model( 
    mass=3.0, 
    substage=sub_stages.SUB_MS_HIMASS, 
    model_start=250, 
    model_example=300, 
    model_end=348, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=3.0") 

MODEL_3_0_HGAP = MESA_model( 
    mass=3.0, 
    substage=sub_stages.SUB_POSTMS_HGAP, 
    model_start=348, 
    model_example=363, 
    model_end=380, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=3.0") 

MODEL_3_0_RG = MESA_model( 
    mass=3.0, 
    substage=sub_stages.SUB_RG, 
    model_start=380, 
    model_example=400, 
    model_end=430, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=3.0") 

MODEL_3_0_HESTABLE = MESA_model( 
    mass=3.0, 
    substage=sub_stages.SUB_HEIGN_STABLE, 
    model_start=430, 
    model_example=433, 
    model_end=435, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=3.0") 

MODEL_3_0_HEMS = MESA_model( 
    mass=3.0, 
    substage=sub_stages.SUB_HEMS, 
    model_start=435, 
    model_example=650, 
    model_end=950, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=3.0") 

MODEL_3_0_AGB = MESA_model( 
    mass=3.0, 
    substage=sub_stages.SUB_AGB, 
    model_start=950, 
    model_example=1700, 
    model_end=11000, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=3.0") 

MODEL_3_0_COWD = MESA_model( 
    mass=3.0, 
    substage=sub_stages.SUB_WD_CO, 
    model_start=None, 
    model_example=None, 
    model_end=None, 
    MESA_folder_path=file_paths.MESA_data_folder/"M=3.0") 


################################################################################

ALL_MODELS_LIST = misc.CustomList([ 
    MODEL_0_2_NONE, 
    MODEL_0_2_HAYASHI,
    MODEL_0_2_MS, 
    MODEL_0_2_HEWD, 

    MODEL_0_4_NONE, 
    MODEL_0_4_HAYASHI, 
    MODEL_0_4_MS, 
    MODEL_0_4_SUBGIANT, 
    MODEL_0_4_RG,
    MODEL_0_4_HEWD, 

    MODEL_1_0_NONE, 
    MODEL_1_0_HAYASHI,
    MODEL_1_0_HENYEY, 
    MODEL_1_0_MS, 
    MODEL_1_0_SUBGIANT, 
    MODEL_1_0_RG, 
    MODEL_1_0_HEFLASH,
    MODEL_1_0_HEMS,
    MODEL_1_0_AGB, 
    MODEL_1_0_COWD, 

    MODEL_1_75_NONE, 
    MODEL_1_75_HAYASHI,
    MODEL_1_75_HENYEY, 
    MODEL_1_75_MS, 
    MODEL_1_75_HGAP, 
    MODEL_1_75_RG, 
    MODEL_1_75_HEFLASH,
    MODEL_1_75_HEMS,
    MODEL_1_75_AGB, 
    MODEL_1_75_COWD, 

    MODEL_3_0_NONE, 
    MODEL_3_0_HAYASHI,
    MODEL_3_0_HENYEY, 
    MODEL_3_0_MS, 
    MODEL_3_0_HGAP, 
    MODEL_3_0_RG, 
    MODEL_3_0_HESTABLE,
    MODEL_3_0_HEMS,
    MODEL_3_0_AGB, 
    MODEL_3_0_COWD 
]) 


################################################################################

