import { AITool } from '../types';
import {
    productDescriptionGenerator, productTitleOptimizer, ecommerceAdCopyGenerator,
    collectionDescriptionGenerator, customerReviewResponse, ecommerceFaqGenerator,
    shippingPolicyGenerator, returnPolicyGenerator, upsellCrossSellGenerator,
    seoProductOptimizer
} from './ecommerce/batch1-critical';
import {
    priceComparisonCopy, productLaunchCopy, seasonalPromotionGenerator,
    loyaltyProgramCopy, cartAbandonmentPopup, productComparisonTable,
    sizeGuideGenerator, productQaGenerator, inventoryAlertCopy,
    giftGuideGenerator
} from './ecommerce/batch2-high-priority';
import {
    supplierEmailTemplate, wholesaleInquiryResponse, dropshippingProductCopy,
    marketplaceListingOptimizer, printOnDemandDescription
} from './ecommerce/batch3-medium-priority';

export const ecommerceTools: AITool[] = [
    productDescriptionGenerator,
    productTitleOptimizer,
    ecommerceAdCopyGenerator,
    collectionDescriptionGenerator,
    customerReviewResponse,
    ecommerceFaqGenerator,
    shippingPolicyGenerator,
    returnPolicyGenerator,
    upsellCrossSellGenerator,
    seoProductOptimizer,
    priceComparisonCopy,
    productLaunchCopy,
    seasonalPromotionGenerator,
    loyaltyProgramCopy,
    cartAbandonmentPopup,
    productComparisonTable,
    sizeGuideGenerator,
    productQaGenerator,
    inventoryAlertCopy,
    giftGuideGenerator,
    supplierEmailTemplate,
    wholesaleInquiryResponse,
    dropshippingProductCopy,
    marketplaceListingOptimizer,
    printOnDemandDescription
];
