import { RecommendationResponse, ManualRecommendationResponse } from "../types/recommendation";

const API_BASE_URL = "http://127.0.0.1:8000";
const ORACLE_APEX_BASE_URL = "https://g57a5a6c122b36a-hackathonconecta.adb.us-chicago-1.oraclecloudapps.com/ords/hackathonconecta";

export class RecommendationService {
	static async getRecommendations(
		clientId: string,
		topK: number = 5
	): Promise<RecommendationResponse> {
		try {
			const response = await fetch(
				`${API_BASE_URL}/recommendations/${clientId}?top_k=${topK}`
			);

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const data = await response.json();
			return data;
		} catch (error) {
			console.error("Error fetching recommendations:", error);
			throw error;
		}
	}

	static async getManualRecommendations(clientId: string): Promise<ManualRecommendationResponse> {
		try {
			const response = await fetch(
				`${ORACLE_APEX_BASE_URL}/clients/${clientId}/recommendations/manual`
			);

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const data = await response.json();
			return data;
		} catch (error) {
			console.error("Error fetching manual recommendations:", error);
			throw error;
		}
	}

	static async healthCheck(): Promise<boolean> {
		try {
			const response = await fetch(`${API_BASE_URL}/health`);
			return response.ok;
		} catch (error) {
			console.error("Health check failed:", error);
			return false;
		}
	}
}
