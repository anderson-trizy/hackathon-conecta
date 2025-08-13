export interface RecommendationProduct {
	id: string;
	name: string;
	description: string;
	score: number;
	category: string;
	segment: string;
	isCompanyRecommended?: boolean;
	isManualRecommendation?: boolean;
	manualRecommendationType?: "CLIENTE" | "PERSONA" | "TORRE";
	similarCompaniesCount?: number;
	benefits?: string[];
	image?: string;
	detailedDescription?: string;
	keyFeatures?: string[];
	technicalSpecs?: { label: string; value: string }[];
	successStories?: {
		companyName: string;
		industry: string;
		result: string;
		metric: string;
		testimonial: string;
		contactName: string;
		contactRole: string;
	}[];
	resources?: {
		type: "pdf" | "video" | "demo";
		title: string;
		description: string;
		url: string;
	}[];
}

// Interface para dados vindos da API
export interface ApiRecommendationItem {
	product_name: string;
	confidence: number;
	reason?: string;
	similarity_strength?: number;
	avg_similarity?: number;
	avg_fit_score?: number;
	id?: string;
	name?: string;
	description?: string;
	score?: number;
	category?: string;
	segment?: string;
}

export interface RecommendationResponse {
	client_id: string;
	recommendations: ApiRecommendationItem[];
	total: number;
	source?: string;
	algorithm?: string;
	timestamp?: string;
	features_used?: string;
	scoring?: string;
	status?: string;
}

// Interface para recomendações manuais do Oracle APEX
export interface ManualRecommendationItem {
	id: number;
	nome: string;
	createdat: string;
	tiporecomendacao: "CLIENTE" | "PERSONA" | "TORRE";
}

export interface ManualRecommendationResponse {
	items: ManualRecommendationItem[];
	hasMore: boolean;
	limit: number;
	offset: number;
	count: number;
	links: Array<{
		rel: string;
		href: string;
	}>;
}
