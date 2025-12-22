import numpy as np
from dataclasses import dataclass, field
from typing import Literal, Callable
from .const import Z0, EPS0
from .lib import EISO, EOMNI

@dataclass
class FarFieldComponent:
    F: np.ndarray

    @property
    def x(self) -> np.ndarray:
        return self.F[0,:]
    
    @property
    def y(self) -> np.ndarray:
        return self.F[1,:]
    
    @property
    def z(self) -> np.ndarray:
        return self.F[2,:]
    
    @property
    def theta(self) -> np.ndarray:
        thx = np.cos(self.theta)*np.cos(self.phi)
        thy = np.cos(self.theta)*np.sin(self.phi)
        thz = -np.sin(self.theta)
        return thx*self.F[0,:] + thy*self.F[1,:] + thz*self.F[2,:]
    
    @property
    def phi(self) -> np.ndarray:
        phx = -np.sin(self.phi)
        phy = np.cos(self.phi)
        phz = np.zeros_like(self.theta)
        return phx*self.F[0,:] + phy*self.F[1,:] + phz*self.F[2,:]
    
    @property
    def rhcp(self) -> np.ndarray:
        return (self.theta + 1j*self.phi)/np.sqrt(2)
    
    @property
    def lhcp(self) -> np.ndarray:
        return (self.theta - 1j*self.phi)/np.sqrt(2)
    
    @property
    def AR(self) -> np.ndarray:
        R = np.abs(self.rhcp)
        L = np.abs(self.lchp)
        return (R+L)/(R-L)
    
    @property
    def norm(self) -> np.ndarray:
        return np.sqrt(np.abs(self.F[0,:])**2 + np.abs(self.F[1,:])**2 + np.abs(self.F[2,:])**2)
    
@dataclass
class EHFieldFF:
    _E: np.ndarray
    _H: np.ndarray
    theta: np.ndarray
    phi: np.ndarray
    Ptot: float
    ang: np.ndarray | None = None
    
    def total_radiated_power_integral(
        self,
        r: float = 1.0,
        use: str = "EH",              # "EH" or "E"
        degrees: bool | None = None,  # auto if None
    ) -> float:
        E = np.asarray(self._E)
        H = np.asarray(self._H)
        th = np.asarray(self.theta, float)
        ph = np.asarray(self.phi, float)

        if E.shape[:1] != (3,) or E.ndim != 3:
            raise ValueError(f"_E must be (3,N,M), got {E.shape}")
        if th.shape != E.shape[1:] or ph.shape != E.shape[1:]:
            raise ValueError(f"theta/phi must be (N,M) matching _E[1:], got {th.shape}, {ph.shape}")
        if use.upper() == "EH" and H.shape != E.shape:
            raise ValueError(f"_H must match _E for use='EH', got {H.shape}")

        if degrees is None:
            degrees = (np.nanmax(th) > 2*np.pi + 0.5) or (np.nanmax(ph) > 2*np.pi + 0.5)
        if degrees:
            th = np.deg2rad(th)
            ph = np.deg2rad(ph)

        # rhat(θ,φ)
        rhat = np.stack(
            [np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)],
            axis=0,
        )  # (3,N,M)

        # S_r
        if use.upper() == "EH":
            S = 0.5 * np.real(
                np.cross(np.moveaxis(E, 0, -1), np.conj(np.moveaxis(H, 0, -1)))
            )  # (N,M,3)
            Sr = np.sum(S * np.moveaxis(rhat, 0, -1), axis=-1)  # (N,M)
        elif use.upper() == "E":
            Sr = (np.sum(np.abs(E) ** 2, axis=0) / (2.0 * Z0)).real  # (N,M)
        else:
            raise ValueError("use must be 'EH' or 'E'")

        # dΩ for general (θ(i,j), φ(i,j)) grid: dΩ = sinθ * |∂(θ,φ)/∂(i,j)| di dj
        dth_di, dth_dj = np.gradient(th, edge_order=2)
        dph_di, dph_dj = np.gradient(ph, edge_order=2)
        J = dth_di * dph_dj - dth_dj * dph_di  # ∂(θ,φ)/∂(i,j)
        dOmega = np.sin(th) * np.abs(J)

        return float(r**2 * np.sum(Sr * dOmega))
    
    @property
    def E(self) -> np.ndarray:
        return FarFieldComponent(self._E)
    
    @property
    def H(self) -> np.ndarray:
        return FarFieldComponent(self._H)
    
    @property
    def Ex(self) -> np.ndarray:
        return self._E[0,:]
    
    @property
    def Ey(self) -> np.ndarray:
        return self._E[1,:]
    
    @property
    def Ez(self) -> np.ndarray:
        return self._E[2,:]
    
    @property
    def Hx(self) -> np.ndarray:
        return self._H[0,:]
    
    @property
    def Hy(self) -> np.ndarray:
        return self._H[1,:]
    
    @property
    def Hz(self) -> np.ndarray:
        return self._H[2,:]
    
    @property
    def Etheta(self) -> np.ndarray:
        thx = np.cos(self.theta)*np.cos(self.phi)
        thy = np.cos(self.theta)*np.sin(self.phi)
        thz = -np.sin(self.theta)
        return thx*self._E[0,:] + thy*self._E[1,:] + thz*self._E[2,:]
    
    @property
    def Ephi(self) -> np.ndarray:
        phx = -np.sin(self.phi)
        phy = np.cos(self.phi)
        phz = np.zeros_like(self.theta)
        return phx*self._E[0,:] + phy*self._E[1,:] + phz*self._E[2,:]
    
    @property
    def Erhcp(self) -> np.ndarray:
        return (self.Etheta + 1j*self.Ephi)/np.sqrt(2)
    
    @property
    def Elhcp(self) -> np.ndarray:
        return (self.Etheta - 1j*self.Ephi)/np.sqrt(2)
    
    @property
    def AR(self) -> np.ndarray:
        R = np.abs(self.Erhcp)
        L = np.abs(self.Elhcp)
        return (R+L)/(R-L)
    
    @property
    def gain(self, kind: Literal['iso','omni'] = 'iso') -> FarFieldComponent:
        if kind=='iso':
            return FarFieldComponent(self._E/EISO)
        else:
            return FarFieldComponent(self._E/EOMNI)
        
    @property
    def dir(self, kind: Literal['iso','omni'] = 'iso') -> FarFieldComponent:
        if kind=='iso':
            return FarFieldComponent(self._E/(EISO*(self.Ptot)**0.5))
        else:
            return FarFieldComponent(self._E/(EOMNI*(self.Ptot)**0.5))
    
    @property
    def normE(self) -> np.ndarray:
        return np.sqrt(np.abs(self._E[0,:])**2 + np.abs(self._E[1,:])**2 + np.abs(self._E[2,:])**2)
    
    @property
    def normH(self) -> np.ndarray:
        return np.sqrt(np.abs(self._H[0,:])**2 + np.abs(self._H[1,:])**2 + np.abs(self._H[2,:])**2)
    
    
    def surfplot(self, 
             polarization: Literal['Ex','Ey','Ez','Etheta','Ephi','normE','Erhcp','Elhcp','AR'],
             quantity: Literal['abs','real','imag','angle'] = 'abs',
             isotropic: bool = True, dB: bool = False, dBfloor: float = -30, rmax: float | None = None,
             offset: tuple[float, float, float] = (0,0,0)) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Returns the parameters to be used as positional arguments for the display.add_surf() function.

        Example:
        >>> model.display.add_surf(*dataset.field[n].farfield_3d(...).surfplot())

        Args:
            polarization ('Ex','Ey','Ez','Etheta','Ephi','normE'): What quantity to plot
            isotropic (bool, optional): Whether to look at the ratio with isotropic antennas. Defaults to True.
            dB (bool, optional): Whether to plot in dB's. Defaults to False.
            dBfloor (float, optional): The dB value to take as R=0. Defaults to -10.

        Returns:
            tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: The X, Y, Z, F values
        """
        fmap = {
            'abs': np.abs,
            'real': np.real,
            'imag': np.imag,
            'angle': np.angle,
        }
        mapping = fmap.get(quantity.lower(),np.abs)
        
        F = mapping(getattr(self, polarization))
        
        if isotropic:
            F = F/np.sqrt(Z0/(2*np.pi))
        if dB:
            F = 20*np.log10(np.clip(np.abs(F), a_min=10**(dBfloor/20), a_max = 1e9))-dBfloor
        if rmax is not None:
            F = rmax * F/np.max(F)
        xs = F*np.sin(self.theta)*np.cos(self.phi) + offset[0]
        ys = F*np.sin(self.theta)*np.sin(self.phi) + offset[1]
        zs = F*np.cos(self.theta) + offset[2]

        return xs, ys, zs, F

@dataclass
class EHField:
    _E: np.ndarray
    _H: np.ndarray
    x: np.ndarray
    y: np.ndarray
    z: np.ndarray
    freq: float
    er: np.ndarray | None = field(default=None)
    ur: np.ndarray | None = field(default=None)
    aux: dict[str, np.ndarray] = field(default_factory=dict)
    

    @property
    def Ex(self) -> np.ndarray:
        return self.E[0,:]
    
    @property
    def Ey(self) -> np.ndarray:
        return self.E[1,:]
    
    @property
    def Ez(self) -> np.ndarray:
        return self.E[2,:]
    
    @property
    def Hx(self) -> np.ndarray:
        return self.H[0,:]
    
    @property
    def Hy(self) -> np.ndarray:
        return self.H[1,:]
    
    @property
    def Hz(self) -> np.ndarray:
        return self.H[2,:]
    
    @property
    def k0(self) -> float:
        return self.freq*2*np.pi/299792458
    
    @property
    def Px(self) -> np.ndarray:
        return EPS0*(self.er-1)*self.Ex
    
    @property
    def Py(self) -> np.ndarray:
        return EPS0*(self.er-1)*self.Ey
    
    @property
    def Pz(self) -> np.ndarray:
        return EPS0*(self.er-1)*self.Ez
    
    @property
    def Dx(self) -> np.ndarray:
        return self.Ex*self.er
    
    @property
    def Dy(self) -> np.ndarray:
        return self.Ey*self.er
    
    @property
    def Dz(self) -> np.ndarray:
        return self.Ez*self.er
    
    @property
    def Bx(self) -> np.ndarray:
        return self.Hx/self.ur
    
    @property
    def By(self) -> np.ndarray:
        return self.Hy/self.ur
    
    @property
    def Bz(self) -> np.ndarray:
        return self.Hz/self.ur
    
    @property
    def Emat(self) -> np.ndarray:
        return self.E
    
    @property
    def Hmat(self) -> np.ndarray:
        return self.H
    
    @property
    def Pmat(self) -> np.ndarray:
        return np.array([self.Px, self.Py, self.Pz])
    
    @property
    def Bmat(self) -> np.ndarray:
        return np.array([self.Bx, self.By, self.Bz])
    
    @property
    def Dmat(self) -> np.ndarray:
        return np.array([self.Dx, self.Dy, self.Dz])
    
    @property
    def Smat(self) -> np.ndarray:
        return np.array([self.Sx, self.Sy, self.Sz])
    
    @property
    def Smmat(self) -> np.ndarray:
        return np.array([self.Smx, self.Smy, self.Smz])
    
    @property
    def EH(self) -> tuple[np.ndarray, np.ndarray]:
        ''' Return the electric and magnetic field as a tuple of numpy arrays '''
        return self.E, self
    
    @property
    def E(self) -> np.ndarray:
        ''' Return the electric field as a numpy array '''
        return self._E
    
    @property
    def H(self) -> np.ndarray:
        ''' Return the magnetic field as a numpy array '''
        return self._H
    
    @property
    def Exyz(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        ''' Return the electric field as a tuple of numpy arrays '''
        return self.Ex, self.Ey, self.Ez
    
    @property
    def Sx(self) -> np.ndarray:
        return self.Ey*self.Hz - self.Ez*self.Hy
    
    @property
    def Sy(self) -> np.ndarray:
        return self.Ez*self.Hx - self.Ex*self.Hz
    
    @property
    def Sz(self) -> np.ndarray:
        return self.Ex*self.Hy - self.Ey*self.Hx
    
    @property
    def Smx(self) -> np.ndarray:
        return 0.5*(self.Ey*np.conj(self.Hz) - self.Ez*np.conj(self.Hy))
    
    @property
    def Smy(self) -> np.ndarray:
        return 0.5*(self.Ez*np.conj(self.Hx) - self.Ex*np.conj(self.Hz))
    
    @property
    def Smz(self) -> np.ndarray:
        return 0.5*(self.Ex*np.conj(self.Hy) - self.Ey*np.conj(self.Hx))
    
    @property
    def B(self) -> np.ndarray:
        ''' Return the magnetic field as a numpy array '''
        return np.array([self.Bx, self.By, self.Bz])
    
    @property
    def Bxyz(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        ''' Return the magnetic field as a tuple of numpy arrays '''
        return self.Bx, self.By, self.Bz
    
    @property
    def Pxyz(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        ''' Return the polarization field as a tuple of numpy arrays '''
        return self.Px, self.Py, self.Pz

    @property
    def P(self) -> np.ndarray:
        ''' Return the polarization field as a numpy array '''
        return np.array([self.Px, self.Py, self.Pz])
    
    @property
    def D(self) -> np.ndarray:
        ''' Return the electric displacement field as a numpy array '''
        return np.array([self.Dx, self.Dy, self.Dz])
    
    @property
    def Dxyz(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        ''' Return the electric displacement field as a tuple of numpy arrays '''
        return self.Dx, self.Dy, self.Dz

    @property
    def Hxyz(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        ''' Return the magnetic field as a tuple of numpy arrays '''
        return self.Hx, self.Hy, self.Hz

    @property
    def S(self) -> np.ndarray:
        ''' Return the poynting vector field as a numpy array '''
        return np.array([self.Sx, self.Sy, self.Sz])
    
    @property
    def Sxyz(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        ''' Return the poynting vector field as a tuple of numpy arrays '''
        return self.Sx, self.Sy, self.Sz
    
    @property
    def Sm(self) -> np.ndarray:
        ''' Return the poynting vector field as a numpy array '''
        return np.array([self.Smx, self.Smy, self.Smz])
    
    @property
    def Smxyz(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        ''' Return the poynting vector field as a tuple of numpy arrays '''
        return self.Smx, self.Smy, self.Smz
    
    @property
    def normE(self) -> np.ndarray:
        """The complex norm of the E-field
        """
        return np.sqrt(np.abs(self.Ex)**2 + np.abs(self.Ey)**2 + np.abs(self.Ez)**2)
    
    @property
    def normH(self) -> np.ndarray:
        """The complex norm of the H-field"""
        return np.sqrt(np.abs(self.Hx)**2 + np.abs(self.Hy)**2 + np.abs(self.Hz)**2)
    
    @property
    def normP(self) -> np.ndarray:
        """The complex norm of the P-field
        """
        return np.sqrt(np.abs(self.Px)**2 + np.abs(self.Py)**2 + np.abs(self.Pz)**2)
    
    @property
    def normB(self) -> np.ndarray:
        """The complex norm of the B-field
        """
        return np.sqrt(np.abs(self.Bx)**2 + np.abs(self.By)**2 + np.abs(self.Bz)**2)
    
    @property
    def normD(self) -> np.ndarray:
        """The complex norm of the D-field
        """
        return np.sqrt(np.abs(self.Dx)**2 + np.abs(self.Dy)**2 + np.abs(self.Dz)**2)
    
    @property
    def normS(self) -> np.ndarray:
        """The complex norm of the S-field
        """
        return np.sqrt(np.abs(self.Sx)**2 + np.abs(self.Sy)**2 + np.abs(self.Sz)**2)
    
    def _get_quantity(self, field: str, metric: str) -> np.ndarray:
        field_arry = getattr(self, field)
        if metric=='abs':
            field = np.abs(field_arry)
        elif metric=='real':
            field = field_arry.real
        elif metric=='imag':
            field = field_arry.imag
        elif metric=='complex':
            field = field_arry
        else:
            field = field_arry
        return field
    
    def vector(self, field: Literal['E','H'], metric: Literal['real','imag','complex'] = 'real') -> tuple[np.ndarray, np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray]:
        """Returns the X,Y,Z,Fx,Fy,Fz data to be directly cast into plot functions.

        The field can be selected by a string literal. The metric of the complex vector field by the metric.
        For animations, make sure to always use the complex metric.

        Args:
            field ('E','H'): The field to return
            metric ([]'real','imag','complex'], optional): the metric to impose on the field. Defaults to 'real'.

        Returns:
            tuple[np.ndarray,...]: The X,Y,Z,Fx,Fy,Fz arrays
        """
        Fx, Fy, Fz = getattr(self, field)
        
        if metric=='real':
            Fx, Fy, Fz = Fx.real, Fy.real, Fz.real
        elif metric=='imag':
            Fx, Fy, Fz = Fx.imag, Fy.imag, Fz.imag
        
        return self.x, self.y, self.z, Fx, Fy, Fz
    
    def scalar(self, field: Literal['Ex','Ey','Ez','Hx','Hy','Hz','normE','normH'] | str, metric: Literal['abs','real','imag','complex'] = 'real') -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Returns the data X, Y, Z, Field based on the interpolation

        For animations, make sure to select the complex metric.

        Args:
            field (str): The field to plot
            metric (str, optional): The metric to impose on the plot. Defaults to 'real'.

        Returns:
            (X,Y,Z,Field): The coordinates plus field scalar
        """
        if field in self.aux:
            field_arry = self.aux[field]
        else:
            field_arry = getattr(self, field)
        
        if metric=='abs':
            field = np.abs(field_arry)
        elif metric=='real':
            field = field_arry.real
        elif metric=='imag':
            field = field_arry.imag
        elif metric=='complex':
            field = field_arry
        return self.x, self.y, self.z, field_arry

    def int(self, field: str | Callable, metric: Literal['abs','real','imag','complex',''] = '') -> float | complex:
        if isinstance(field, Callable):
            field = field(self)
        else:
            field = self._get_quantity(field, metric)
        if len(field.shape)==2:
            axis = 1
        else:
            axis = 0
        return np.sum(field*self.aux['areas']*self.aux['weights'], axis=axis)