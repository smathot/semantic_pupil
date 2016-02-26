## Materials and availability

Participant data, experimental scripts, and analysis scripts are available from <https://github.com/smathot/semantic_pupil>.

## Stimuli

We manually selected 121 words from Lexique [@New2004], a large database with lexical properties of French words. There were four word categories: brightness-conveying words (e.g. *illuminé* or 'illuminated'; *N*=33), darkness-conveying words (e.g. *foncé* or 'dark'; *N*=33), neutral words (e.g. *renforcer* or 're-inforce'; *N*=35), and animal names (e.g. *lapin* or 'rabbit'; *N*=20). During the experiments, words were shown as dark letters (8.5 cd/m^2^) against a gray background (17.4 cd/m^2^).

Because we wanted to compare the pupillary responses to brightness- and darkness-conveying words, these two categories needed to be matched as accurately as possible. We focused on two main properties: lexical frequency, how often a word occurs in books (bright: M=41 per million, SD=147; dark: M=39, SD=119); and visual intensity (bright: M=1.58x10^6^ arbitrary units, SD=4.31x10^5^; dark: M=1.56x10^6^, SD=4.26x10^5^). Visual intensity was matched by selecting words that had approximately the same number of letters, then generating images of these words, and finally iteratively resizing these images until the visual intensity (i.e. summed luminance) of the words was almost identical between the two categories.

In the end, we had a stimulus set in which darkness- and brightness-conveying words were very closely matched; however, as a result of our stringent criteria, our set contained several variations of the same words, such as *briller* ('to shine') and *brillant* ('shining'). But given the pupil's sensitivity to slight differences in task difficulty (i.e. lexical frequency) and visual intensity, we felt that matching was more important than having a highly varied stimulus set.

## Pupillometry experiment

Thirty naive observers (age range: 18-54 y; 21 women) participated in the experiment. Participants reported normal or corrected vision, provided written informed consent prior to the experiment, and received €6 for their participation. The experiment was conducted with approval of the *Comité d'éthique de l'Université d'Aix-Marseille* (Ref.: 2014-12-03-09).

Pupil size was recorded monocularly with an EyeLink 1000 (SR Research, Missisauga, Ontario, Canada), a video-based eye tracker sampling at 1000 Hz. Stimuli were presented on a 21" ViewSonic p227f CRT monitor (1024 x 768 px, 150 Hz). Testing took place in a dimly lit room. The experiment was implemented with OpenSesame [@MathôtSchreijTheeuwes2012] using the Expyriment [@KrauseLindemann2014] backend.

At the beginning of each session, a nine-point eye tracker calibration was performed. Before each trial, a single-point recalibration (drift correction) was performed. Each trial started with a dark central fixation dot on a gray background for 3 s. Next, a word was presented centrally for 3 s, or until the participant pressed the space bar. The participant's task was to press the space bar whenever an animal name was presented, and to withhold response otherwise. Participants saw each word once, with the exception of *pénombre* which, due to a bug in the experiment, was shown twice. (This is why there are slightly more darkness- than brightness-conveying trials, as shown in %FigMainResults.) Word order was fully randomized.

## Normative ratings

For each word, we collected normative ratings from thirty naive observers (age range: 18-29 y; 17 women), most of whom had not participated in the pupillometry experiment. Participants received €2 for their participation.

Words were presented, one at a time and using the same images as used for the pupillometry experiment, together with a five-point rating scale. On this scale, participants indicated how strongly the word conveyed a sense of brightness ('Very bright' to 'very dark'), or, in a different phase of the experiment, the word's valence ('Very negative' to 'very positive'). Brightness and valence were rated in separate blocks, the order of which was counterbalanced across participants. Based on valence ratings, we calculated the emotional intensity of the words, as the deviation from neutral valence (Intensity = |3-valence|).
