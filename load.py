
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


def setPoint(x, y, z, valx, valy, valz):

    max_x,max_y,max_z = max(x)+valx,max(y)+valy,max(z)+valz
    min_x,min_y,min_z = min(x)-valx,min(y)-valy,min(z)-valz

    pointx= [max_x,max_x,max_x,max_x,min_x,min_x,min_x,min_x]
    pointy= [max_y,max_y,min_y,min_y,max_y,max_y,min_y,min_y]
    pointz= [max_z,min_z,min_z,max_z,max_z,min_z,min_z,max_z]

    
    return pointx, pointy, pointz

def drawLine(ax, px, py, pz):
    for i in range(8):      
        if i == 3 or i == 7:
            ax.plot([px[i], px[i-3]], [py[i],py[i-3]],zs=[pz[i],pz[i-3]])
        
        else:
            ax.plot([px[i], px[i+1]], [py[i],py[i+1]],zs=[pz[i],pz[i+1]])
           
        if i < 4:
            ax.plot([px[i], px[i+4]], [py[i],py[i+4]],zs=[pz[i],pz[i+4]])
           
    return ax


def drawFigure(x, y, z, distance_x, distance_y, distance_z):

    ran = [abs(max(x)), abs(min(x)),abs(max(y)), abs(min(y)),abs(max(z)), abs(min(z))]
    min_range = -int(max(ran)*1.34) 
    max_range = int(max(ran)*1.34) 

    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_zlim(min_range, max_range)
    ax.set_ylim(min_range, max_range)
    ax.set_xlim(min_range, max_range)
    ax.scatter(x, y, z,  marker='o', s=5, cmap='Greens')


    for i in [0, 0.1, 0.34]:
        pointx, pointy, pointz = setPoint(x, y, z, distance_x * i ,distance_y*i, distance_z * i)
        ax.scatter(pointx, pointy, pointz, marker='o', s=30, cmap='Greens')
        ax = drawLine(ax, pointx, pointy, pointz)

    
    plt.show()


def calCordinate(flename):
    stpfile = open(filename, mode='rt', encoding='cp949')

    x = []
    y = []
    z = []
    val = []
    vertex = []

    transform_value = 1000
    datastart = False

    while True:
        data = stpfile.readline().rstrip()
        
        if data == "END-ISO-10303-21;":
            break

        elif data == "DATA;":
            datastart = True
            continue
        
        elif data == "End;":
            datastart = False


        if datastart is True:
            number = data.split("=")[0].rstrip()
            
            if not number[0] is "#":
                continue 
            
            content = ""
            
            if "=" in data:
                content = data.split("=")[1].lstrip()
                content = content.split("(")
            else:
                continue

            
            if content[0] == "VERTEX_POINT":
                command = content[0]
                number = content[1].split(")")[0]
                number = number.split(",")[1]
                
                vertex.append(number)
                


            #if content[0] == "VECTOR":
                #transform_value = float(content[4].split(",")[0])
            
            if content[0] == "CARTESIAN_POINT":
                command = content[0]
                cord = content[2].split(")")
                cord = cord[0].split(",")

                x_cord = float(cord[0])
                y_cord = float(cord[1])
                z_cord = -1
               
                if cord[2] == '':
                    nextdata = stpfile.readline().rstrip()
                    z_cord_miss = float(nextdata.split(")")[0])
                    z_cord = z_cord_miss
                else:
                    z_cord = float(cord[2])

                   
                dic = {'number':"", 'command':"", 'value':[]}
                dic['number'] = number
                dic['command'] = command
                dic['value']= [x_cord, y_cord, z_cord]
                

                val.append(dic)
                

    realWorldCord = float(1000 / transform_value)
    
    for dic_i in val:   
        if dic_i['number'] in vertex:
            x.append(realWorldCord * dic_i['value'][0])
            y.append(realWorldCord * dic_i['value'][1])
            z.append(realWorldCord * dic_i['value'][2])
   
    return x, y, z
    

datalist = ["/home/jwsi/pre_study/realfile/chameleon-top_cap_assy_190417.stp",
            "/home/jwsi/pre_study/realfile/chameleon_bottom_cap_190417.stp",
            "/home/jwsi/pre_study/realfile/chameleon_bottom_cap_bracket_190417.stp",
            "/home/jwsi/pre_study/realfile/chameleon_collar_190417.stp",
            "/home/jwsi/pre_study/realfile/chameleon_ui_button_asm_190417.stp"]

if __name__ == "__main__":
    filename = datalist[2]
    x, y, z = calCordinate(filename)


    
    depth = abs(max(x)-min(x))
    width = abs(max(y)-min(y))
    height = abs(max(z)-min(z))

    drawFigure(x, y, z, depth, width, height)

    prodVol = width*height*depth
    coreVol = width*height*depth*(1.2**3)
    moldVol = width*height*depth*(1.68**3)
    
    print("filename  : " + filename)

    print("[Product]")
    print("Width : {:.4f} mm".format(width))
    print("Height: {:.4f} mm".format(height))
    print("Depth : {:.4f} mm".format(depth))
    print("Volume: {:.4f} mm^2".format(prodVol))

    print("[Core]")
    print("Width : {:.4f} mm".format(width*1.2))
    print("Height: {:.4f} mm".format(height*1.2))
    print("Depth : {:.4f} mm".format(depth*1.2))
    print("Volume: {:.4f} mm^2".format(coreVol))

    print("[Mold]")
    print("Width : {:.4f} mm".format(width*1.68))
    print("Height: {:.4f} mm".format(height*1.68))
    print("Depth : {:.4f} mm".format(depth*1.68))
    print("Volume: {:.4f} mm^2".format(moldVol))

    print("전체의 비중 7.8, KP1소재 (단가 2550원) 가정 시, 소숫점 첫째자리에서 반올림")
    
    weight = 7.8
    unitPrice = 2550
    exchange = 1000000

    prodPrice = round((prodVol*weight/exchange)*unitPrice,0)
    corePrice = round((coreVol*weight/exchange)*unitPrice,0)
    moldPrice = round((moldVol*weight/exchange)*unitPrice,0)
    print("Product : {:.0f}".format(prodPrice))
    print("Core : {:.0f}".format(corePrice))
    print("Mold : {:.0f}".format(moldPrice))

