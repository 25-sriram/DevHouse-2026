import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000'
});

export const getDashboardOverview = async () => {
    const response = await API.get('/dashboard/overview');
    return response.data;
};

export const getRequirementDetails = async (id) => {
    const response = await API.get(`/dashboard/requirement/${id}`);
    return response.data;
};

export const getContribution = async (id) => {
    const response = await API.get(`/analytics/contributions/${id}`);
    return response.data;
};

export const getEffort = async (id) => {
    const response = await API.get(`/analytics/effort/${id}`);
    return response.data;
};

export const getImpact = async (id) => {
    const response = await API.get(`/analytics/impact/${id}`);
    return response.data;
};

export const getWorkload = async () => {
    const response = await API.get('/analytics/workload');
    return response.data;
};

export const getKnowledgeRisk = async () => {
    const response = await API.get('/analytics/knowledge-risk');
    return response.data;
};

export const getBusinessSummary = async (id) => {
    const response = await API.get(`/analytics/business-summary/${id}`);
    return response.data;
};

export const recomputeAnalytics = async (id) => {
    // Assuming backend endpoint exists for recomputation, if not this is a placeholder
    const response = await API.post(`/analytics/recompute/${id}`);
    return response.data;
};
