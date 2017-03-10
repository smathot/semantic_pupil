---
title: "Pupillary responses to words that convey a sense of brightness or darkness (Supplementary Information)"
author:
  Sebastiaan Mathôt^1,2^\*, Jonathan grainger^2^, Kristof Strijkers^3^
affiliation:
  - ^1^ University of Groningen, Department of Experimental Psychology, Groningen, Netherlands
  - ^1^ Aix-Marseille University, CNRS, LPC UMR 7290, Marseille, France
  - ^2^ Aix-Marseille University, CNRS, LPL UMR 7309, Aix-en-Provence, France
  - \* Corresponding author
correspondence:
  - Grote Kruisstraat 2/1
  - 9712 TS Groningen
  - Netherlands
---


# Robustness checks

To verify that our main conclusions do not depend on the specifics of the analyses, we conducted several alternative analyses, or 'robustness checks.'


## Main analysis

In the original analysis (described in the main text), we conducted separate LMEs for each 10 ms, using the following model (in the style of the R package `lme4`):

	pupil_size ~ word_category + (1+word_category|subject_nr)

Here, *word_category* was a discrete factor with two levels (bright or dark). For this original analyses, we excluded neutral words, because neutral words were not matched to the darkness- and brightness-conveying words.

As a robustness check, we used the following alternative model:

	pupil_size ~ rating_brightness + (1+rating_brightness|subject_nr)

Here, *rating_brightness* was a continuous predictor corresponding to the brightness of the words as rated by the participants on a scale from 1 to 5. We now also included neutral words. Crucially, also when analyzing the effect of semantic brightness in this way, the effect of rating_brightness was highly robust (see %FigModelComparison)


## Individual-participant analysis

In the original analysis, we looked at mean pupil size during the 1 - 2 s window for each participant, and tested whether pupil size was larger for darkness- than brightness-conveying words using a Bayesian one-sided paired-samples t test.

As a robustness check, we tested whether this difference also holds when considering mean pupil size during the entire 3 s window of word presentation. When changing the analysis window, but keeping the analysis otherwise identical, there was again evidence for an effect in both the visual (Bf = 51.3) and (some in the) auditory (BF = 1.8) experiment (combined BF = 93.6, or 'very strong evidence').


## Individual-word analysis

In the original analysis, we looked at mean pupil size during the 1 - 2 s window for each word, and tested whether pupil size was larger for darkness- than brightness-conveying words using a Bayesian one-sided independent samples t test.

As a robustness check, we tested whether this difference also holds when considering mean pupil size during the entire 3 s window of word presentation. When changing the analysis window, but keeping the analysis otherwise identical, there was again evidence for an effect in both the visual (Bf = 5.2) and (some in the) auditory (BF = 2.2) experiment (combined BF = 11.6, or 'strong evidence').


# Model comparisons

To test how well the semantic brightness, emotional intensity, and valence of the words (as rated by the participants) predicted pupil size, we conducted separate LMEs for each 10 ms window, using the following models (in the style of the R package `lme4`):

	pupil_size ~ rating_brightness + (1+rating_brightness|subject_nr)
	pupil_size ~ rating_intensity + (1+rating_intensity|subject_nr)
	pupil_size ~ rating_valence	+ (1+rating_valence|subject_nr)

Here, *rating_brightness*, *rating_intensity*, and *rating_valence* are the subjective word ratings, as described in the Methods of the main text. (We used three separate models with a single predictor, rather than a single model with three predictors, because the high correlations between ratings would cause a combined model to produce a misleading impression of what the actual data looks like.) The results are shown in %FigModelComparison, in which the absolute t values (as a proxy for effect size) are plotted for each of the predictors as a function of time from word onset:


%--
figure:
  id: FigModelComparison
  source: FigModelComparison.svg
  caption: |
   The absolute t values of the fixed effect of rated brightness, valence, and emotional intensity as a function of time from word onset. a) Results for the visual experiment. b) Results for the auditory experiment.
--%


A few things are clear from %FigModelComparison.

First, the t values of `rating_brightness` and `rating_valence` are highly correlated. This is to be expected, because brightness and valence ratings were highly correlated (r=.89; described in the main text). This correlation is too high to allow a meaningful statistical dissociation (for example through partial effects) between brightness and valence ratings. For this reason we conducted a control experiment (described below) in which we measured the pupillary response to words that varied in valence, but not in semantic brightness.

Second, and more importantly for the present study, during the interval of the semantic pupil effect, emotional intensity does not, or hardly, predict pupil size.


## Control experiment: The effect of valence on pupillary responses

The details of the control experiment are described in the main text. In summary, we measured pupillary responses to positive and negative words that did not have any obvious association with brightness. If the results of our main experiments had been confounded by valence (positive/ negative), this control experiment should show that the pupil is larger in response to negative words, compared to positive words.

As shown in %FigControl, this is not we found: Valence has no notable effect on pupil size.


%--
figure:
  id: FigControl
  source: FigControl.svg
  caption: |
    a) Pupil size over time, as a function of whether a positive (e.g. 'cadeau' or 'present') or negative (e.g. 'cicatrice' or 'scar') word was presented. Error bands are standard errors. The vertical dotted line indicates the mean response time to animal words. b) The difference in mean pupil size during the 1 - 2 s window between positive and negative words for individual participants. c) Mean pupil size during the 1 - 2 s for individual positive and negative words.
--%


However, as shown in %FigIntensity, emotional intensity does affect pupil size in a graded manner, such that the pupil was largest for words of high intensity, intermediate for words of medium intensity, and smallest for words of low intensity. (Important note: Words of different intensities were not matched on various important properties, and it is therefore possible that the effect of emotional intensity is mediated by another variable that correlates with emotional intensity.)


%--
figure:
  id: FigIntensity
  source: FigIntensity.svg
  caption: |
    a) Pupil size over time, as a function of whether a word of high, medium, or low emotional intensity was presented (based on a split into three equally sized bins). Error bands are standard errors.
--%
