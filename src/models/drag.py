import numpy as np
#using mach number, find drag coefficents using barrowman method.
#depending on mach num, select appropiate drag model. this is, for now, barrowman supersonic and barrowman subsonic. 
def barrowman_drag(mach_num):
    #SKIN DRAG SECTION
    Cd=None #coefficent of drag for entire vehicle
    Cf=None #incompressible skin friction coefficent
    Cf_c = None #compressible skin finction coefficent
    R_s = 0.2 / 1000 #surface roughness height. Assumed to be 0.2mm, converted into meters
    ref_l = None #length of vehicle from tip to tail
    mu = None #dynamic viscosity of air - atm model based.
    rho = None #density of air - atm model based.
    u = None #flow velocity - atm model based.
    Re = rho*u*ref_l/mu #Reynolds number
    a= None #Speed of sound - atm model based.
    Ma = u/a #Mach number 
    L = None #tip to tail length
    D = None #fuselage OD
 
    #incompressible fluid between Mach 0.0 and 0.3
    if (Ma > 0 and Ma<0.3):
        #incompressible laminar flow
        if (Re<=500000): 
            Cf=1.328/np.sqrt(Re)
        #incompressible turbulent flow
        else:
            #Re_cr is the Reynolds number at which skin friction does not matter. This is the threshold between what is considered smooth and rough.
            Re_cr=51*(R_s/ref_l)**-1.039
            if Re>Re_cr:
                Cf=0.032(R_s/ref_l)**0.2
            else:
                Cf = (1/(3.45*np.log10(Re)-5.6)**2)-(1700/Re)
    #compressible subsonic variation
    elif (Ma>=0.3 and Ma<1): 
        #checking smooth vs rough cases (Re_cr comparison)
        if (Re_cr>Re): 
            Cf_c = Cf(1-0.9*Ma**2)
        else:
            Cf_c = Cf(1-0.12*Ma**2)
    else:
        #if laminar
        if (Re<=500000):
            Cf_c=Cf/((1+0.045*Ma**2)**0.25)
        else:
            #if smooth
            if (Re_cr>Re):
                #k is defined as the coefficent for the no heat transfer case. This is reccomended from the man himself. Equ. 4-12
                k=0.15
                Cf_c=Cf/((1+k*Ma**2)**0.58)
            else:
                Cf_c=Cf/(1+0.18*Ma**2)
                #handling a case where roughness is less than smoothness value. this should NEVER be the case. if so, set value to smooth value regardless. 
                if(Cf_c<Cf/((1+k*Ma**2)**0.58)):
                    Cf_c=Cf/((1+k*Ma**2)**0.58)

    #Defining skin friction drag coefficent of the tail section
    Ar = None #reference area
    AT = None #planform area of fins
    AwB = None #wetted area of body
    N = None #Fin qty. 
    fB= L/D #body fineness ratio. basically L/D ignoring finspan
    Cd_fT = 2*N*Cf_c*(AT/Ar) #skin friction coefficent of drag for fins
    Cd_fB = (1+0.5/fB)*Cf_c*AwB/Ar #skin friction coefficent of drag for body

    #PRESSURE DRAG SECTION
    #Tail Pressure Drag
    S = None #exposed fin semispan measured from root chord. basically perpendicular distance from fuselage to outside edge of fin.
    Ar_fins = None 
    DeltaCd = None
    rL = None #this is the radius of the leading edge of the fins
    GammaL = None #leading edge sweep angle in degrees

#determining the DeltaCd factor based on Mach number. Pg. 50 Barrowman's
    if (Ma<0.9):
        DeltaCd = ((1-Ma**2)**-0.417)-1
    elif (Ma>=0.9 and Ma<=1):
        DeltaCd = 1-1.5(Ma-0.9)
    else:
        DeltaCd = 1.214 - 0.502/Ma**2 + 0.1095/Ma**4 + 0.0231/Ma**6

#total leading drag edge of N amount of fins
    Cd_LTail=2*N*(S*rL/Ar_fins)*(np.cos(np.deg2rad(GammaL))**2)*DeltaCd

#trailing edge drag for subsonic incompressible flow

    Cd_BTail=None
    Cr = None #fin root chord length
    hr = None #fin trailing edge thickness
    ABf = None #base area of one fin
    CfB = 2*Cf_c*(Cr/hr) #Compressible skin friction coefficent for the body
    tr = None #Max thickness of fin

    if (Ma > 0 and Ma<0.3):
        CfB=2*Cf*(Cr/hr)
        Cd_BTail = 0.135/(CfB**(1/3))
    #trailing edge drag for subsonic compressible flow
    elif (Ma>=0.3 and Ma<1):
        K_prandtl_correction = np.cos(np.deg2rad(GammaL))**2 + ((0.223+4.02*Cf_c*(tr/hr))**2/(Cf_c*Cr/hr)**(2/3))
        Cd_BTail = (0.135*N*(ABf/Ar_fins))/((CfB**(1/3))*(K_prandtl_correction-np.cos(np.deg2rad(GammaL))**2*Ma**2)**0.5)
    #trailing edge drag for supersonic compressible flow
    else:
        Cd_BTail = (N*(1-0.52*Ma**-1.19))*(ABf/Ar_fins)/((1+18*Cf_c*(tr/hr)**2)*Ma**2)
    
# 















