# -*- coding: utf-8 -*-
"""Catch22 features.

A transformer for the Catch22 features using the pycatch22 C wrapper.
"""

__author__ = ["MatthewMiddlehurst"]
__all__ = ["Catch22Wrapper"]

import numpy as np
import pandas as pd
import pycatch22

from sktime.transformations.base import BaseTransformer


class Catch22Wrapper(BaseTransformer):
    """Canonical Time-series Characteristics (Catch22) C Wrapper.

    Wraps the pycatch22 implementation for sktime
    (https://github.com/DynamicsAndNeuralSystems/pycatch22).

    Overview: Input n series with d dimensions of length m
    Transforms series into the 22 Catch22 [1]_ features extracted from the hctsa [2]_
    toolbox.

    features : str or List of str, optional, default="all"
        The Catch22 features to extract by name. If "all", all features are extracted.
    replace_nans : bool, optional, default=True
        Replace NaN or inf values from the Catch22 transform with 0.

    See Also
    --------
    Catch22 Catch22Classifier

    References
    ----------
    .. [1] Lubba, C. H., Sethi, S. S., Knaute, P., Schultz, S. R., Fulcher, B. D., &
    Jones, N. S. (2019). catch22: Canonical time-series characteristics. Data Mining
    and Knowledge Discovery, 33(6), 1821-1852.
    .. [2] Fulcher, B. D., Little, M. A., & Jones, N. S. (2013). Highly comparative
    time-series analysis: the empirical structure of time series and their methods.
    Journal of the Royal Society Interface, 10(83), 20130048.
    """

    _tags = {
        "scitype:transform-input": "Panel",
        "scitype:transform-output": "Primitives",
        "scitype:instancewise": True,
        "X_inner_mtype": "numpy3D",
        "y_inner_mtype": "None",
        "fit_is_empty": True,
        "python_dependencies": "pycatch22",
    }

    def __init__(
        self,
        features="all",
        replace_nans=False,
    ):
        self.features = features
        self.replace_nans = replace_nans

        super(Catch22Wrapper, self).__init__()

    def _transform(self, X, y=None):
        """Transform data into the Catch22 features.

        Parameters
        ----------
        X : 3D numpy array of shape [n_instances, n_dimensions, n_features],
            input time series panel.
        y : ignored.

        Returns
        -------
        c22 : Pandas DataFrame of shape [n_instances, c*n_dimensions] where c is the
             number of features requested, containing Catch22 features for X.
        """
        n_instances, n_dims, _ = X.shape

        if isinstance(self.features, str):
            if self.features == "all":
                f_idx = [i for i in range(22)]
            elif self.features in feature_names:
                f_idx = feature_names.index(self.features)
            else:
                raise ValueError("Invalid feature selection.")
        elif isinstance(self.features, (list, tuple)):
            if len(self.features) > 0 and all(
                [f in feature_names for f in self.features]
            ):
                f_idx = list(
                    dict.fromkeys([feature_names.index(f) for f in self.features])
                )
            else:
                raise ValueError("Invalid feature selection.")
        else:
            raise ValueError("Invalid feature selection.")

        c22 = np.zeros((n_instances, len(f_idx) * n_dims))
        for i in range(n_instances):
            for n in range(n_dims):
                dim = n * len(f_idx)
                series = list(X[i, n, :])
                for j, f in enumerate(f_idx):
                    c22[i][dim + j] = features[f](series)

        if self.replace_nans:
            c22 = np.nan_to_num(c22, False, 0, 0, 0)

        return pd.DataFrame(c22)


feature_names = [
    "DN_HistogramMode_5",
    "DN_HistogramMode_10",
    "SB_BinaryStats_diff_longstretch0",
    "DN_OutlierInclude_p_001_mdrmd",
    "DN_OutlierInclude_n_001_mdrmd",
    "CO_f1ecac",
    "CO_FirstMin_ac",
    "SP_Summaries_welch_rect_area_5_1",
    "SP_Summaries_welch_rect_centroid",
    "FC_LocalSimple_mean3_stderr",
    "CO_trev_1_num",
    "CO_HistogramAMI_even_2_5",
    "IN_AutoMutualInfoStats_40_gaussian_fmmi",
    "MD_hrv_classic_pnn40",
    "SB_BinaryStats_mean_longstretch1",
    "SB_MotifThree_quantile_hh",
    "FC_LocalSimple_mean1_tauresrat",
    "CO_Embed2_Dist_tau_d_expfit_meandiff",
    "SC_FluctAnal_2_dfa_50_1_2_logi_prop_r1",
    "SC_FluctAnal_2_rsrangefit_50_1_logi_prop_r1",
    "SB_TransitionMatrix_3ac_sumdiagcov",
    "PD_PeriodicityWang_th0_01",
]

features = [
    pycatch22.DN_HistogramMode_5,
    pycatch22.DN_HistogramMode_10,
    pycatch22.SB_BinaryStats_diff_longstretch0,
    pycatch22.DN_OutlierInclude_p_001_mdrmd,
    pycatch22.DN_OutlierInclude_n_001_mdrmd,
    pycatch22.CO_f1ecac,
    pycatch22.CO_FirstMin_ac,
    pycatch22.SP_Summaries_welch_rect_area_5_1,
    pycatch22.SP_Summaries_welch_rect_centroid,
    pycatch22.FC_LocalSimple_mean3_stderr,
    pycatch22.CO_trev_1_num,
    pycatch22.CO_HistogramAMI_even_2_5,
    pycatch22.IN_AutoMutualInfoStats_40_gaussian_fmmi,
    pycatch22.MD_hrv_classic_pnn40,
    pycatch22.SB_BinaryStats_mean_longstretch1,
    pycatch22.SB_MotifThree_quantile_hh,
    pycatch22.FC_LocalSimple_mean1_tauresrat,
    pycatch22.CO_Embed2_Dist_tau_d_expfit_meandiff,
    pycatch22.SC_FluctAnal_2_dfa_50_1_2_logi_prop_r1,
    pycatch22.SC_FluctAnal_2_rsrangefit_50_1_logi_prop_r1,
    pycatch22.SB_TransitionMatrix_3ac_sumdiagcov,
    pycatch22.PD_PeriodicityWang_th0_01,
]
