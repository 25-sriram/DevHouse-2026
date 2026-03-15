import React, { createContext, useContext, useState, useCallback } from 'react';
import * as api from '../services/api';

const DashboardContext = createContext();

export const useDashboard = () => useContext(DashboardContext);

export const DashboardProvider = ({ children }) => {
    const [overview, setOverview] = useState(null);
    const [workload, setWorkload] = useState([]);
    const [knowledgeRisk, setKnowledgeRisk] = useState([]);
    const [selectedRequirement, setSelectedRequirement] = useState(null);
    const [contribution, setContribution] = useState(null);
    const [effort, setEffort] = useState(null);
    const [impact, setImpact] = useState(null);
    const [businessSummary, setBusinessSummary] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchGlobalMetrics = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const overviewData = await api.getDashboardOverview();
            const workloadData = await api.getWorkload();
            const riskData = await api.getKnowledgeRisk();
            setOverview(overviewData);
            setWorkload(workloadData);
            setKnowledgeRisk(riskData);
        } catch (err) {
            setError(err.message || 'Error fetching global metrics');
        } finally {
            setLoading(false);
        }
    }, []);

    const fetchRequirementMetrics = useCallback(async (id) => {
        setLoading(true);
        setError(null);
        try {
            const reqData = await api.getRequirementDetails(id);
            const contribData = await api.getContribution(id);
            const effortData = await api.getEffort(id);
            const impactData = await api.getImpact(id);
            const busSumm = await api.getBusinessSummary(id);
            
            setSelectedRequirement(reqData);
            setContribution(contribData);
            setEffort(effortData);
            setImpact(impactData);
            setBusinessSummary(busSumm);
        } catch (err) {
            setError(err.message || 'Error fetching requirement metrics');
        } finally {
            setLoading(false);
        }
    }, []);

    const refreshAnalytics = useCallback(async (id = null) => {
        if (id) {
            await api.recomputeAnalytics(id);
            await fetchRequirementMetrics(id);
        } else {
            await fetchGlobalMetrics();
        }
    }, [fetchGlobalMetrics, fetchRequirementMetrics]);

    const value = {
        overview, workload, knowledgeRisk, selectedRequirement,
        contribution, effort, impact, businessSummary,
        loading, error,
        fetchGlobalMetrics, fetchRequirementMetrics, refreshAnalytics
    };

    return (
        <DashboardContext.Provider value={value}>
            {children}
        </DashboardContext.Provider>
    );
};
