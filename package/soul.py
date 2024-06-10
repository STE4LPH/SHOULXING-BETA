import re
import json
import xml.etree.ElementTree as ET
#from rich import print
class ModArchifrex:
    def __init__(self, path='/data/data/com.ChillyRoom.DungeonShooter'):
        self.path = path
        self.playerPrefs_path = path+'/shared_prefs/com.ChillyRoom.DungeonShooter.v2.playerprefs.xml'
        self.gameData_path = path+'/files/game.data'



    
    @staticmethod
    def __modcharacthers(path, regex, HERO, All) -> None:
        # Cargar el Archivo xml
        tree = ET.parse(path)
        root = tree.getroot()
        # Buscar el elemento String        
        for element in root.findall('string'):
            # Cargar los datos que tienen elelemnto string
            unlock = element.get('name')
            # Busca los en los elemetos que comienzen con 'c'
            if unlock.endswith(f'_c{HERO}_unlock') and not All: # All -> False
                # Cambia su valor Boleano de False a True
                if element.text == 'False':
                    element.text = 'True'
                    # Guarda los cambios modifcados en el archivo
                    tree.write(path, encoding='utf-8', xml_declaration=True)
                                
            elif re.findall(regex, unlock) and All:
                element.text = 'True'
                
                tree.write(path, encoding='utf-8', xml_declaration=True)

                    
    
    
    @staticmethod
    def _GameData(path) -> dict:
        # Clave bytes
        key = [115, 108, 99, 122, 125, 103, 117, 99, 127, 87, 109, 108, 107, 74, 95]
        # abrir el archivo game.data
        with open(path, 'rb') as file:
            cifre_data = file.read()
        # Comvertir en bytearray
        byte_cifre = bytearray(cifre_data)
        # XOR
        for i in range(len(byte_cifre)):
            byte_cifre[i] = key[i % 15] ^ byte_cifre[i]
        
        # Convertir el bytearray a diccionario
        convert = byte_cifre.decode('utf-8')
        json_data = json.loads(convert)        
        
        #Retornar valor de tipo diccionario
        return json_data


# Idea crear decoradores deacodificadores y codificadores
    @staticmethod
    def __progress_data(path) -> str:

        with open(path, 'r+') as file:
            game_data = ModArchifrex._GameData(path)
            hero = list(game_data['heroUnlock'].keys())
            count = 0
            list_hero = ''
            for i in hero:
                var = f'[ {count} ] \033[1;33m{i}\033[0m'
                list_hero += var+'\n'
                count +=1

        return list_hero

    
    @staticmethod
    def __level(path, regex=r'(c\d+_level.*?=")\d+'):
        with open(path, 'r+') as file:
            code = file.read()
            values = re.findall(r'c\d+_level.*?="\d+"', code)
            c_level = ['c0','c2','c3','c5','c8','c10','c14','c15']
            for x in values:
                if x.split('_')[0] in c_level:
                    mod = re.sub(r'(c\d+_level.*?=")\d+',r'\g<1>8',x)
                else:
                    mod = re.sub(r'(c\d+_level.*?=")\d+',r'\g<1>7',x)
                code = code.replace(x, mod)
            file.seek(0)
            file.write(code)
            file.truncate()

    
    @staticmethod
    def __skills_heroe(playerdata, gamedata, hero_name=None, All=None):
        tree = ET.parse(playerdata)
        root = tree.getroot()
        
        with open(playerdata,'r') as file:
            var = file.read()
            id_usuario = re.findall(r'(\d+)(?>_)', var)[0]


        with open(playerdata, 'r+') as file:
            game_data = ModArchifrex._GameData(gamedata)


            #for idx, (x, y) in enumerate(game_data['heroSkillUnlock'].items()):
            #    print(f'[ {idx} ] {x} SkILL')

            for idx, (x,y) in enumerate(game_data['heroSkillUnlock'].items(),1):
                
                if x == hero_name and not All:
                    break; # Esta en mantenimiento
                    for count in range(len(y)):
                        for element in root.findall('int'):
                            unlock = element.get('name')
                            if unlock and unlock.endswith(f'{hero_name}_skill'):
                                if element.get('value') == '0':
                                    element.set('value', '1')
                                    tree.write(playerdata, encoding='utf-8', xml_declaration=True)

                        #print(f'c_{x}_skill_{count}_unlock')
                elif All:
                    for count in range(1, len(y)+1):
                        skills = f'{id_usuario}_c_{x}_skill_{count}_unlock'
                        #print(skills)
                        element_found = False
                        for element in root.findall('int'):
                            unlock = element.get('name')
                        #Verificar si el elemento ya existe
                            if unlock == skills:
                                #Camviar los valores de los encomtrados
                                element.set('value', '1')
                                element_found = True
                                
                            
                        if not element_found:
                            new_element = ET.Element('int', name=skills, value='1')
                                #print(new_element)
                            root.append(new_element)
                            tree.write(playerdata, encoding='utf-8', xml_declaration=True)
        
    
    @staticmethod
    def __ModfishChips():
        pass


class SoulModKnight(ModArchifrex):
    def characters(self,Unlock=None,All=None):
        """ path -> Ruta  
            regex -> codigo
            Heroe -> Numero de Heroe a desbloquearAll
            All -> Desbloqueo de todo los peronsajes
        """
        ModArchifrex._ModArchifrex__modcharacthers(self.playerPrefs_path, r'c\d+_unlock', Unlock, All)
    
    def nameHeroe(self):
        return ModArchifrex._ModArchifrex__progress_data(self.gameData_path)

    def levelHeroe(self):
        ModArchifrex._ModArchifrex__level(self.playerPrefs_path)

    def skillHero(self):
        """
        hero_name -> 'Nombre del heroe a desbloquear'
        All -> Si esta en True Desbloquea todo, si esta
        en false solo desbloquea uno
        """
        ModArchifrex._ModArchifrex__skills_heroe(self.playerPrefs_path, self.gameData_path, hero_name='Knight', All=True)

    
        


# Esta por desarrollo
# Poner los nombres de los personajes bloqueados y hacerlo individualmente
# Crear opcion para dewbloquear a todos

#print(SoulModKnight().nameCharacters())


#SoulModKnight().characters('31')

#SoulModKnight().skillHero()

