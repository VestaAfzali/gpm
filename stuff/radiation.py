"""
This is an self made Library for the Lecture :

Introduction to Atmospheric Radiation and Remote Sensing

The whole contents is from the Lecture 416 and the Book:
A First Course In Atmospheric Radiation
Secon edition
Grant W. Petty


"""


import numpy as np
import math
import matplotlib.pyplot as plt

# Important Global Constants
c = 2.998*10**8         # Lichtgeschindigkeit in m/s
h = 6.626*10**-34       # Plancks Konstante in Js
k = 1.381*10**-23       # Boltzmankonstante in J/K
sigma = 5.67 *10**-8    # Stefan-Boltzmann in W/ m^2 K^4
S = 1370                # Solarkonstante in W/m^2
AU = 150*10**11         # Astronomische Einheit in m
R_Erde = 6356.0         # Erdradius in km
kw = 2897.0             # Wien's Komstante in nm K


def BeerBougetLambert(F, beta, s):
    """
    Function:
         bouguer-lambert-beersche Gesetz beschreibt die Abschwaechung der
         Intensitaet einer Strahlung bei dem Durchgang durch ein Medium
         mit einer absorbierenden Substanz, in Abhaengigkeit von der
         Konzentration der absorbierenden Substanz und der Schichtdicke
    Input:
        F       ::: radiation flux density in W/m2 befor absorption
        beta    ::: volumen absorption coeff.
        s       ::: path length
    Output:
        F_att   ::: radiation flux density in W/m2 after absorption

    """
    F_att = F * np.exp(-1* beta * s)
    return F_att


def beta(ni, lam):
    """
    Function:
         Berechnung des volumen absorptions coeff
    Input:

        ni    ::: refractive Index
        lam   ::: wellenlaenge
    Output:
        beta  ::: absorptions coeff

    """
    beta = (4* math.pi * ni)/lam
    return beta

def micro2m(wav):
    wav_neu = wav*10**-6
    return wav_neu

def freq2wav(freq):
    """frequen in pro sekunde, GHz = 10**9"""
    wave = c / freq
    return wave

def wav2freq(wav):
    """wav in meter"""
    frequenc = c / wav
    return frequenc

def K2C(Kelvin):
    C = Kelvin - 273.15
    return C

def C2K(C):
    Kelvin = C + 273.15
    return Kelvin

def planck(wav, T):
    a1 = (2.0*h*c**2)/(wav**5)
    b1 = (h*c)/(k*T*wav)
    intensity = a1 * 1/(np.exp(b1)-1.0)
    return intensity

def emission(intens, emiss):
    Intens_neu = emiss*intens
    return Intens_neu

def intens2Tb(wav,intens):
    a1 = (2.0*h*c**2)/(intens*wav**5)
    b1 = (h*c)/(k*wav)
    Tb = b1 * 1/(math.log(1.0 + a1))
    return Tb


def wtr(A, T):
    """WattThermalRadiation"""
    W = A * sigma * T**4
    return W

def nhl(A, T1, T2):
    """net Heat loss"""
    W = A * sigma * (T1**4 - T2**4)
    return W

def Teffplanet(A, D):
    Teff = ((S * (1.-A)) / (4.*sigma*D**2.))**(1./4.)
    return Teff

def Teff(A, s):
    Teff = ((s * (1.-A)) / (4.*sigma))**(1./4.)
    return Teff

def SB(S):
    T = (S/sigma)**(1./4.)
    return T

def SB2(T):
    S = sigma*T**4.
    return S

def srtm(asw, alw, A, eps=None):
    """
    Simple radiative transfere model of Atmo
    A ::: Albedo
    asw ::: Absorption kurzwellig
    alw ::: Absorbtion langwellig
    """
    if eps == None:
        Sm = S / 4.
        Esurf = ((1. - (1. - asw) * A) * ((2. - asw)/(2. - alw)))
        Tsurf = (Sm / sigma * (Esurf))**(1./4.)
        Eatmo = (((1 - A) * (1 - asw) * alw) + (1 + (1 - asw) * A) * asw)/((2 - alw) * alw)
        Tatmo = (Sm/sigma * (Eatmo))**(1./4.)
        return Tatmo, Tsurf
    if eps != None:
        eps = eps
        Sm = S / 4.
        Esurf = ((A - 1) * (1 - asw) * (1 + (1 - alw)) * (1 - eps) + eps * (A * (1 - asw)**2)-1)/(eps * (2 - alw))
        Tsurf = (-1* Sm / sigma * (Esurf))**(1./4.)
        Eatmo = (((A - 1) * (1 - asw))*alw + (1 + ((1 - asw) * A))* asw) / (alw * ( eps * (( 1- alw) + 1)) + ((1 - alw) * (1-eps)))
        Tatmo = (-1*Sm/sigma * (Eatmo))**(1./4.)
        return Tatmo, Tsurf


def rainbow_min_def_ang(m, k):
    """
    Computes a minimum angle of deflection for a Rainbow


    Returns
    -------
    angle
    """
    res = np.sqrt((m**2)/(k**2 +2*k))
    res = np.rad2deg(np.arccos(res))

    return res




#Ex6.19a
a_sw = np.arange(0.01,1.0,0.01)
a_lw = np.arange(0.01,1.0,0.01)
Albedo = np.arange(0.01, 1.0, 0.01)
emi = np.arange(0.01, 1.0, 0.01)


# Ex 19a
Ta, Ts = srtm(a_sw, 0.8, 0.3)
plt.plot(a_sw, Ta, label='Ta', color='blue')
plt.plot(a_sw, Ts, label='Ts', color='green' )
plt.ylabel('Temp in K')
plt.xlabel('Absorbiton')
plt.grid()
plt.legend(loc='upper right')
plt.show()

# Ex 19b
Ta, Ts = srtm(0.1, a_lw, 0.3)
plt.plot(a_sw, Ta, label='Ta', color='blue')
plt.plot(a_sw, Ts, label='Ts', color='green' )
plt.ylabel('Temp in K')
plt.xlabel('Absorbiton')
plt.grid()
plt.legend(loc='upper right')
plt.show()

# Ex 19c
Ta, Ts = srtm(0.1, 0.8, Albedo)
plt.plot(a_sw, Ta, label='Ta', color='blue')
plt.plot(a_sw, Ts, label='Ts', color='green' )
plt.ylabel('Temp in K')
plt.xlabel('Albedo')
plt.grid()
plt.legend(loc='upper right')
plt.show()

for i in Albedo:
    Ta, Ts = srtm(a_sw, 0.8, i)
    plt.plot(a_sw, Ta, label='Ta', color='blue')
    plt.plot(a_sw, Ts, label='Ts', color='green' )


plt.ylabel('Temp in K')
plt.xlabel('Absorbiton')
plt.grid()
plt.legend(loc='upper right')
plt.show()

# Ex 19d
Ta, Ts = srtm(0.1, 0.8, 0.3, emi)
plt.plot(emi, Ta, label='Ta', color='blue')
plt.plot(emi, Ts, label='Ts', color='green' )
plt.ylabel('Temp in K')
plt.xlabel('Albedo')
plt.grid()
plt.legend(loc='upper right')
plt.show()


#G.P.?
#plt.plot(w,planck(w,3000))

#GP 6.15
#a) wtr(2,305.2)*0.97
#b) nhl(2, C2K(32), C2K(20))*0.97



# GP 6.11
#T1 = intens2Tb(micro2m(11), planck(micro2m(11),300)*0.95)
#T2 = intens2Tb(0.0158, planck(0.0158,300)*0.95)

# GP 6.20
Ai = np.array([0.11, 0.65, 0.30, 0.15, 0.52, 0.41, 0.30])
Di = np.array([0.39, 0.72, 1.0, 1.52, 5.20, 30.0, 40.0])
for i in range(len(Ai)):
    print Teffplanet(Ai[i] , Di[i])


emi = np.arange(0.,1,0.01)
tempi = np.arange(250,350)
wavi = np.arange(micro2m(0.1),micro2m(7), micro2m(0.01))

for i in emi:
    plt.scatter(i,intens2Tb(0.0158, planck(0.0158,300)*i))


plt.xlabel('Emmision')
plt.ylabel('Temperatur in K')
plt.show()


def calc_S_from_ground(I1, I2, w1, w2):
    """
    GP 7.8 Problem

    I1, I2 gemessene Intensitaeten

    w1, w2 Einfallswinkel in Grad

    """
    ww1 = 1/np.cos(np.deg2rad(w1))
    ww2 = 1/np.cos(np.deg2rad(w2))

    tau = (-1 * np.log(I1/I2)) / (ww1-ww2)
    S0 = I1 * np.exp(tau / np.cos(np.deg2rad(w1)))

    return tau , S0


def atmo_h(z):
    piz = np.exp(-z/8)
    return piz

def atmo_tau_t(z, const=1, winkel=0):
    tau = const * 8 * np.exp(-z/8)
    t =  np.exp(-tau/np.cos(np.deg2rad(winkel)))
    return tau, t

def atmo_w(t, winkel=0):
    tw = np.exp(-z/8)*t/np.cos(np.deg2rad(winkel))
    return tw

def atmo(z):
    tau = np.exp(-z)
    t =  np.exp(-tau)
    return tau, t

for i in np.array([0, 30, 60 ,80]):
    ww = i
    z = np.arange(0,100,0.01)
    tau, t = atmo_tau_t(z, winkel=ww)
    rho = atmo_h(z)
    tw = atmo_w(t, winkel=ww)
    plt.subplot(2,2,1)
    plt.plot(t,z, label='transmission__'+str(ww))
    plt.legend()
    plt.xlim(0,1)
    plt.grid()
    plt.subplot(2,2,4)
    plt.plot(rho,z, label='dichte__'+str(ww))
    plt.legend()
    plt.xlim(0,1)
    plt.grid()
    plt.subplot(2,2,3)
    plt.plot(tau,z, label='optische dicke__'+str(ww))
    plt.legend()
    plt.xlim(0,1)
    plt.grid()
    plt.subplot(2,2,2)
    plt.plot(tw,z, label='gewichtete transmission__'+str(ww))
    plt.legend()
    plt.xlim(0,1)
    plt.grid()


plt.show()

z = np.arange(0,100,0.01)
tau, t = atmo(z)
plt.plot(t,z); plt.plot(tau,z); plt.show()

def taus(ka, w1,rho, H):
    taus = ka * w1 * rho * H
    return taus


def wfunc(z,taus, winkel, H=8):
    mu = 1./np.cos(np.deg2rad(winkel))
    A1 = (taus / (H * mu)) * np.exp(-z/H)
    A2 = np.exp((-taus/mu) * np.exp(-z/H))
    Wz = A1 * A2
    return Wz


def t1(asw,alw,A):
    res1 = (1.-(1.-asw)*A)*(2.-asw) - (1.-asw)*(1.-A)*(2.-alw)
    return res1


######################### AUFGABE
def ts(asw, alw, A, S, sig):
    res1 = (1.-(1.-asw)*A) *((2.-asw)/(2.-alw))
    #res2 = res1 /(2.-alw)*alw
    res3 = ((S/sig)*res1)**(1./4.)
    return res3

def ta(asw, alw, A, S, sig):
    res1 = (1.-A)*(1.-asw)*alw + ((1. + (1.-asw)*A)*asw)
    res2 = res1/((2-alw)*alw)
    res3 = ((S/sig)*res2)**(1./4.)
    return res3


def taa(asw, alw, A, S, sig):
    res1 = (1.-A)*(1.-asw)-(1.- (1. - asw)*A) * ((2.-asw)/(2.-alw))
    res2 = res1/(-1*alw)
    res3 = ((S/sig)*res2)**(1./4.)
    return res3

def gp7_3(t, H):
    """
    H in meter
    """
    beta_e = -1* (math.log(t))/H
    return beta_e


def gp_79(H, k, roh):
    """GP7.9"""
    res = 0.5/(k * roh * H)
    z = -1 * np.log(res) * H
    return z

def gpb(H, k, roh):
    """GP7.9"""
    res = (k * roh * H)/0.5
    z = np.log(res) * H
    return z


def FEstat():
    import numpy as np
    import matplotlib.pyplot as plt
    Uebung = np.arange(1,7,1)
    Quickies = np.array([3,5,6,5,8,5])
    Aufgaben = np.array([2,3,4,2,4,8])
    Program = np.array([1,1,1,1,0,0])
    plt.plot(Uebung, Quickies, label='Quickies')
    plt.plot(Uebung, Aufgaben, label='Aufgaben')
    plt.plot(Uebung, Program, label='Programiereaufgabe')
    plt.xlabel('Uebung')
    plt.ylabel('Anzahl')
    plt.legend('upper left')
    plt.title('Verlauf der Uebungen in FE')
    plt.grid()
    plt.show()


