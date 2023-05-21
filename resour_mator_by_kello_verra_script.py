import os
import json
import sys
import re


'''
  _____  ______  _____  ____  _    _ _____        __  __       _______ ____  _____  
 |  __ \|  ____|/ ____|/ __ \| |  | |  __ \      |  \/  |   /\|__   __/ __ \|  __ \ 
 | |__) | |__  | (___ | |  | | |  | | |__) |_____| \  / |  /  \  | | | |  | | |__) |
 |  _  /|  __|  \___ \| |  | | |  | |  _  /______| |\/| | / /\ \ | | | |  | |  _  / 
 | | \ \| |____ ____) | |__| | |__| | | \ \      | |  | |/ ____ \| | | |__| | | \ \ 
 |_|  \_\______|_____/ \____/ \____/|_|  \_\__   |_|  |_/_/    \_\_|  \____/|_|  \_\
  _                  _   _    _ _   __      __
 | |                | |/ /   | | |  \ \    / /                                      
 | |__  _   _       | ' / ___| | | __\ \  / /__ _ __ _ __ __ _                      
 | '_ \| | | |      |  < / _ \ | |/ _ \ \/ / _ \ '__| '__/ _` |                     
 | |_) | |_| |      | . \  __/ | | (_) \  /  __/ |  | | | (_| |                     
 |_.__/ \__, |      |_|\_\___|_|_|\___/ \/ \___|_|  |_|  \__,_|                     
         __/ |                                                                      
        |___/                                                                                                                              

Frame per frame animation with ease!

Version 1.0.0 ALPHA
'''

class unicode:
    def __init__(self, value1:int, value2:int, value3:int, value4:int):
        self.valid=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
        self.value= [value1, value2, value3, value4]
        self.verify()

    def verify(self):
        length=len(self.valid)-1
        accum=0
        rev=self.value.copy()
        rev.reverse()
        self.value=[]
        for i in rev:
            if accum != 0:
                i+=accum
                accum=0
            while i > length:
                i-=length
                accum+=1
            self.value.append(i)
        self.value.reverse()
        
        return self
    
    def to_str_arr(self):
        ind=0
        val=['', '', '', '']
        for i in self.value:
            val[ind]=self.valid[i]
            ind+=1         
        return val
    
    def to_str(self):
        string=self.to_str_arr()
        concat=""
        for i in string:
            concat+=i
        return r"\u"+concat

    def inc(self, amount=1):
        self.value[len(self.value)-1]+=amount
        return self.verify()

class libr:
    def __init__(self):
        # SAVED SCOPE
        self.advanced_settings={
            "frame_limit":"0",
            "ascent":"16",
            "height":"0",
            "char_amount":"1",
            "font_sequence_function":"0"
        }
        
        self.advanced_settings_font={
            "frame_limit":"0",
            "ascent":"16",
            "height":"0",
            "char_amount":"1",
            "font_sequence_function":"0"
        }

        self.advanced_settings_model={
            "frame_limit":"0",
            "parent_model":"16",
            "model_sequence_function":"0"
        }

        self.config_skip=False

        self.os_path=os.getcwd()
        self.input_namespace=""
        self.input_namespace_path=""
        self.output_namespace=""
        self.output_namespace_path=""

        self.texture_sequence_name=""
        self.texture_path=""
        self.font_seq_path=""

        self.texture_resourcelocation_dir=""
        self.texture_sequence=[]
        self.font_resourcelocation_dir=""
        self.font_sequence=[]
        self.texture_sequence_dir=""

        self.advanced_initialization=False
        self.font_seq_name = "font"

        # TEMPORARY SCOPE
        self.config_file_path = os.path.join(self.os_path,"resourmator_config.json")
        self.config_avaibility = os.path.isfile(self.config_file_path)
        self.path_validity = "resourcepacks" in str(self.os_path) and "assets" in str(self.os_path)




# helper func

def parsebool(val) -> bool:
    return val in [ "true","1","yes","ye","y","yep","valid","yeah","yeh","ok","agree","of course","why not?","why not" ]

# cant think of a better solution

def import_config(libr:libr):
    with open(os.path.join(libr.config_file_path), "r") as confile:
        dict=json.loads(confile.read())

        try:
            libr.input_namespace=dict["config"]["input_namespace"]
            libr.output_namespace=dict["config"]["output_namespace"]
            libr.input_namespace_path=dict["config"]["input_namespace_path"]
            libr.output_namespace_path=dict["config"]["output_namespace_path"]

            libr.texture_path=dict["config"]["texture_path"]
            libr.texture_sequence_dir=dict["config"]["texture_sequence_dir"]
            libr.texture_resourcelocation_dir=dict["config"]["texture_resourcelocation_dir"]
            libr.font_seq_name=dict["config"]["font_sequence_name"]
            libr.font_seq_path=dict["config"]["font_sequence_path"]
            libr.font_sequence=dict["config"]["font_sequence"]
            libr.font_resourcelocation_dir=dict["config"]["font_resourcelocation_dir"]
            libr.texture_sequence=dict["config"]["texture_sequence"]
            libr.advanced_initialization=dict["config"]["advanced"]

            libr.advanced_settings["frame_limit"]=dict["advanced"]["font"]["frame_limit"]
            libr.advanced_settings["ascent"]=dict["advanced"]["font"]["ascent"]
            libr.advanced_settings["height"]=dict["advanced"]["font"]["height"]
            libr.advanced_settings["char_amount"]=dict["advanced"]["font"]["char_amount"]
            libr.advanced_settings["font_sequence_function"]=dict["advanced"]["font"]["generate_mcfunction"]
        except KeyError:
            print("ERROR : Unknown key, open the editor!")
            libr.config_avaibility=False

def export_config(libr:libr):
    with open(libr.config_file_path, "w") as confile:
        dict={"config":{},"advanced":{"font":{},"model":{}}}

        dict["config"]["input_namespace"]=libr.input_namespace
        dict["config"]["output_namespace"]=libr.output_namespace
        dict["config"]["input_namespace_path"]=libr.input_namespace_path
        dict["config"]["output_namespace_path"]=libr.output_namespace_path

        dict["config"]["texture_path"]=libr.texture_path
        dict["config"]["texture_sequence_dir"]=libr.texture_sequence_dir
        dict["config"]["texture_resourcelocation_dir"]=libr.texture_resourcelocation_dir
        dict["config"]["font_sequence_name"]=libr.font_seq_name
        dict["config"]["font_sequence_path"]=libr.font_seq_path
        dict["config"]["font_sequence"]=libr.font_sequence
        dict["config"]["font_resourcelocation_dir"]=libr.font_resourcelocation_dir
        dict["config"]["texture_sequence"]=libr.texture_sequence
        dict["config"]["advanced"]=libr.advanced_initialization

        dict["advanced"]["font"]["frame_limit"]=libr.advanced_settings["frame_limit"]
        dict["advanced"]["font"]["ascent"]=libr.advanced_settings["ascent"]
        dict["advanced"]["font"]["height"]=libr.advanced_settings["height"]
        dict["advanced"]["font"]["char_amount"]=libr.advanced_settings["char_amount"]
        dict["advanced"]["font"]["generate_mcfunction"]=libr.advanced_settings["font_sequence_function"]
        confile.write(json.dumps(dict,indent=4))

def export_font_sequence_func(libr:libr):
    with open(os.path.join(libr.os_path,libr.font_seq_name+"_sequence.mcfunction"), "w") as mcfunc:
        total_frame=len(libr.font_sequence)
        frame=0
        mcfunc.write("#> Generated using resour-mator by KelloVerra v.1.0.0 ALPHA\n")
        mcfunc.write("#> Replace :\n")
        mcfunc.write("#> <YOUR-TIMER-SCOREBOARD>\n")
        mcfunc.write("#> <YOUR-ENTITY-TAG>\n\n")
        mcfunc.write(f"execute unless score @s <YOUR-TIMER-SCOREBOARD> = @s <YOUR-TIMER-SCOREBOARD> run scoreboard players set @s <YOUR-TIMER-SCOREBOARD> {total_frame}\n")
        mcfunc.write(f"scoreboard players remove @s <YOUR-TIMER-SCOREBOARD> 1\n")
        for font in libr.font_sequence:
            mcfunc.write(f"execute if score @s {frame} run"+" data merge entity @s {text:'{\"text\":\"\\ue000\",\"font\":\""+font+str(frame)+"\"}'}\n")
            frame+=1

        mcfunc.write(f"#execute if score @s {frame+1} run <EVENT-AFTER-SEQUENCE-FINISHED>\n")
            





def init(libr:libr):
    
    # Initialization
    print("##### >> Welcome Back! Time for another debug << #####\n")

    if libr.config_avaibility:
        config_skip = parsebool(input("found config file, automatically set values and skip initialization process? "))
        if config_skip:
            libr.config_skip=config_skip
            return

    if libr.path_validity:

        # Namespaces 
        # Input

        namespaces= [x for x in os.listdir(libr.os_path)
                        if os.path.isdir(os.path.join(libr.os_path,x))]
        namedictionary={}
        print("INFO : Found namespaces: ")
        ind=0
        for name in namespaces:
            namedictionary[ind]=name
            print(f"{ind} : {name}")
            ind+=1
        import_id=int(input("which one might contains the preferred texture to import? (listed number) >> "))
        libr.input_namespace = namedictionary[import_id]
        libr.input_namespace_path = os.path.join(libr.os_path, namedictionary[import_id])
        export_id=int(input("with the namespaces listed above, where will the font sequence be exported? (listed number) >> "))
        libr.output_namespace = namedictionary[export_id]
        libr.output_namespace_path = os.path.join(libr.os_path, namedictionary[export_id])

        # I/O insertion
        # Input

        libr.texture_sequence_dir = os.path.join(libr.os_path,libr.input_namespace,"textures","font","generated_sequence")
        
        if not os.path.isdir(libr.texture_sequence_dir):
            os.makedirs(libr.texture_sequence_dir,exist_ok=False)
            input("INFO : The font sequence directory has been created, you can place your texture sequence containing folder(s) there (enter) ")
        
        # check if texture sequence dir is empty and let the user know to place their sequence folder there
        texture_sequence_list= [x for x in os.listdir(libr.texture_sequence_dir)
                                    if os.path.isdir(os.path.join(libr.texture_sequence_dir,x))]
        while not texture_sequence_list:
            input(f"WARN : Can not found a single texture sequence, please put all of your texture animation sequence inside a folder and put it in [{libr.texture_sequence_dir}] (enter) ")
            texture_sequence_list = [x for x in os.listdir(libr.texture_sequence_dir)
                                    if os.path.isdir(os.path.join(libr.texture_sequence_dir,x))]
        sequence_dictionary={}
        print("INFO : Found texture sequences: ")
        ind=0
        for name in texture_sequence_list:
            sequence_dictionary[ind]=name
            print(f"{ind} : {name}")
            ind+=1
        

        textureind=int(input("insert your preferred texture sequence (listed number) >> "))
        libr.texture_path=os.path.join(libr.texture_sequence_dir,sequence_dictionary[textureind])
        libr.texture_resourcelocation_dir= libr.texture_path.replace("\\","/").split(namedictionary[import_id]+"/textures/")
        libr.texture_path+="\\"
        if len(libr.texture_resourcelocation_dir) >= 2:
            libr.texture_resourcelocation_dir=f"{libr.input_namespace}:{str(libr.texture_resourcelocation_dir[len(libr.texture_resourcelocation_dir)-1])}"
        
        texture_sequences= [x for x in os.listdir(libr.texture_path)
                                    if os.path.isfile(os.path.join(libr.texture_path,x)) and x.endswith('.png')]
        while not texture_sequences:
            input(f"WARN : Can not found a single texture file, please put all of your texture animation sequence inside [{libr.texture_path}] (enter) ")
            texture_sequences = [x for x in os.listdir(libr.texture_path)
                                    if os.path.isdir(os.path.join(libr.texture_path,x)) and x.endswith('.png')]
            
        # string sort thanks to 'https://stackoverflow.com/questions/33159106/sort-filenames-in-directory-in-ascending-order'
        texture_sequences.sort(key=lambda f: int(re.sub('\D', '', f)))
            
        libr.texture_sequence=[libr.texture_resourcelocation_dir+"/"+i for i in texture_sequences]

        # I/O insertion
        # Output

        font_seq=input("name your font animation sequence (string) >> ")
        libr.font_seq_path=os.path.join(libr.output_namespace_path,"font",font_seq)
        libr.font_seq_name=font_seq
        libr.font_resourcelocation_dir= libr.font_seq_path.replace("\\","/").split(namedictionary[export_id])
        if len(libr.font_resourcelocation_dir) >= 2:
            font_string_resourcelocation=str(libr.font_resourcelocation_dir[len(libr.font_resourcelocation_dir)-1]).replace("/font/","")
            libr.font_resourcelocation_dir=f"{libr.output_namespace}:{font_string_resourcelocation}/"
        print(libr.font_resourcelocation_dir)

        # Advanced

        libr.advanced_initialization=parsebool(input("almost there, would you like to tweak some advanced options? "))
        if libr.advanced_initialization:
            skip = False
            exce=False
            while not skip:
                if not exce:
                    print("\n")
                print("Found advanced settings:")
                print("0 : skip operation")
                ind=1
                exce=False
                valdict={}
                for i in libr.advanced_settings.keys():
                    valdict[ind] = i
                    print(f"{ind} : {i} = {libr.advanced_settings[i]}")
                    ind+=1
                try:
                    indinput=int(input("(listed number) >> "))
                except Exception:
                    print("expected an integer but recieved otherwise!")
                    exce=True
                    continue
                if indinput > 0:
                    valueinput=input(valdict[indinput]+" (string) >> ")
                    libr.advanced_settings[valdict[indinput]] = valueinput
                else:
                    skip=True
                    print("skipped advanced settings")

        

    else:
        input("ERROR : The path where this script resides is invalid! Put this script inside the resourcepacks/<YOUR-RESOURCEPACK>/assets and try again, exiting app...")
        sys.exit()

    export_config(libr)

def find(libr:libr):
    pass

def read(libr:libr):
    if libr.config_avaibility:
        import_config(libr)

def gen(libr:libr):
    if libr.config_skip:
        if not os.path.isdir(libr.texture_sequence_dir):
            os.makedirs(libr.texture_sequence_dir,exist_ok=True)

    ind=0
    os.makedirs(os.path.join(libr.font_seq_path),exist_ok=True)

    for i in libr.texture_sequence:
        with open(os.path.join(libr.font_seq_path,str(ind)+".json"), "w") as font:
            ascent=0
            height=16
            chars=["\\ue000"]
            if libr.advanced_initialization:
                ascent=libr.advanced_settings["ascent"]
                height=libr.advanced_settings["height"]
                fontcode=unicode(14,0,0,0)
                chars=[]
                for k in range(int(libr.advanced_settings["char_amount"])):
                    chars.append(fontcode.to_str())
                    fontcode.inc()

                # edgecase where chars are empty
                if not chars:
                    chars=["\\ue000"]

            ''' Okay listen here, the reason i made hardcoded a json writer instead of json.dumps() is that 
                the zen and peace of json.dumps() actually converts \ to \\ which is *super* annoying.
                Ive decided that hardcoding a text file with a .json extension is the way to go and 
                I might implement a custom json writer soon instead, who knows it works for now and for most of the use cases.
            '''
            libr.font_sequence.append(libr.font_resourcelocation_dir)
            font.write("{\n\t\"providers\":[\n\t\t{\n\t\t\t\"type\": \"bitmap\",\n\t\t\t\"file\": \""+i+"\",\n\t\t\t\"ascent\": "+str(ascent)+",\n\t\t\t\"height\": "+str(height)+",\n\t\t\t\"chars\": [\n\t\t\t\t\""+'",\n\t\t\t\t"'.join(chars)+"\"\n\t\t\t]\n\t\t}\n\t]\n}")
        ind+=1

    if parsebool(libr.advanced_settings["font_sequence_function"]):
        export_font_sequence_func(libr)

# The main quintet

library = libr()

find(library)
read(library)
init(library)
gen(library)

input("\nINFO : Generation success!")