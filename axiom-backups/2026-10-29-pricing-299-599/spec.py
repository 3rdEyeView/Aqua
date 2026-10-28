# 2026-10-29: Essentials $297 -> $299, Growth $597 -> $599, Growth advertising-spend disclaimer (owner's exact wording).
import json, re
DISCLAIMER = ('Advertising spend is not included. We recommend considering approximately $500/month to start, but your '
              'advertising budget is flexible and paid separately to Google and/or Meta.')
KEY = {'e-paragraph': 'paragraph', 'e-heading': 'title', 'e-button': 'text'}
def price(t): return t.replace('$297', '$299').replace('$597', '$599')
# Wording changes beyond the price swap (old text is asserted to match the backup exactly, after the price swap).
EDITS = {
 952: {
  '705da915': ('$0 setup fee · First month due at signup · Google Ads spend paid separately to Google',
               '$0 setup fee · First month due at signup · Advertising spend not included'),
  '515a1ed2': ('Google Ads spend is paid separately, directly to Google.',
               'Advertising spend is not included and is paid separately to Google and/or Meta.'),
 },
 1068: {
  '4aa219b8': ('Google Ads advertising spend is not included in the $599 subscription. You pay your advertising budget directly to Google. 3-month minimum commitment; cancellation terms are set out in your service agreement.',
               'The $599 subscription covers setup and standard management only. 3-month minimum commitment; cancellation terms are set out in your service agreement.'),
  '2d707ba5': ('Paid separately to Google', 'Not included · paid separately'),
  '3f79b119': ('Advertising spend is billed separately and paid directly by you through Google Ads.', DISCLAIMER),
 },
 1074: {
  '1a720fb3': ('Google Ads advertising spend is not included in the Growth subscription and is paid directly by you through Google Ads. ', ''),
 },
 1085: {
  '5bd9860e': ('With Growth, your Google Ads advertising spend is separate and paid directly to Google.',
               'With Growth, advertising spend is not included and is paid separately to Google and/or Meta.'),
  '639f7a31': ('Is the Google Ads budget included?', 'Is the advertising budget included?'),
  '213ba1d': ('No. Google Ads advertising spend is not included in the $599 Growth subscription. You choose your advertising budget and pay it directly to Google through your Google Ads account. Your Growth subscription covers the setup and ongoing management of one standard Google Search advertising program.',
              'No. ' + DISCLAIMER + ' Your $599 Growth subscription covers the setup and standard ongoing management of one Google Search advertising program.'),
  '6a103e47': ('Your advertising spend is paid directly to Google and isn\'t included in the subscription.', DISCLAIMER),
 },
 1095: {
  '6508d7ca': ('(includes Google Ads management)', '(includes Google Ads management; ad spend paid separately)'),
 },
}
