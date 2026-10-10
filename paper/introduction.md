# 1 Introduction

Diffusion models [1, 2, 3] and sequence-design networks [4, 5] now propose enzymes far faster than anyone can test them. A single design problem yields tens of thousands to millions of candidates: 130,000 backbones for a cysteine hydrolase designed with RFdiffusion3 [3], several hundred thousand sequences for a zinc metallohydrolase [6], $10^5$ to $10^6$ designs per starting structure for Kemp eliminases [7]. The experiment takes up about a hundred of them, one or two 96-well plates, and the choice is made by an in-silico filter. Richter and colleagues described the task in 2011 as "analyzing, and ranking all of the produced structures to find the best handful worth experimentally characterizing" [8]. <!-- src: Butcher 2025 SI 4.1.1 (130,000 scaffolds generated; 190 designs ordered); Kim 2026 SI "Analysis and filtering of designed sequences" (several hundred thousand design sequences across hundreds of scaffolds; 96 ordered per round); Listov 2025 Methods (10^5 to 10^6 designs for each starting structure; 73 tested); Richter 2011, stage 3 (verbatim). Other campaigns: 129 + 192 designs (Lauko 2025), 36 + 63 (Braun 2026), 48 to 96 per reaction (Ahern 2026), 320 (Anishchenko 2025) -->

Authors credit filtering for part of the recent rise in success rates. Adding a filter for the preorganization of the catalytic residues raised the fraction of serine-hydrolase designs with ester-hydrolysis activity from 1.6% to 5.2% [9], and iterative filtering of predicted catalytic geometry gave 18% multi-turnover cysteine hydrolases, against 1–2% in earlier campaigns [3]. The same filters decide which method is judged better: RFdiffusion2 is reported to pass its in-silico criteria for all 41 active sites of its benchmark, RFdiffusion for 16 [2]. Yet passing the filter does not guarantee activity. Of the 192 designs tested in the metallohydrolase campaign, 176 have no reported kcat/KM [6]. <!-- src: Lauko 2025 main text (round 1 filtered with AF2 alone, round 2 with AF2 then PLACER; 2 of 129 = 1.6% and 10 of 192 = 5.2% with ester hydrolysis; probe-labelled 3% to 17%); Butcher 2025 SI 4.1 (35 of 190 = 18% multi-turnover; earlier one-shot campaigns 1-2%); Ahern 2026 (at least one scaffold passing the success filters for 41/41 cases, RFdiffusion 16/41); Kim 2026 and this paper Results 3.1.2 (192 designs, 16 with a reported kcat/KM). Other changes were made between rounds of these campaigns, hence "credit" -->

The metrics that do the filtering differ between pipelines. Some rank designs by Rosetta energies and shape complementarity [6, 7, 10], some by how closely a predicted structure reproduces the intended catalytic geometry [3, 11], and others by the confidence of AlphaFold or Chai-1 models of the enzyme–substrate complex [12, 13, 14] or by the preorganization of the active site in an ensemble of predicted conformations [9, 15]. Many pipelines combine several of these into a composite score [3, 6, 7]. Cut-offs differ from campaign to campaign, and the weights are set by judgement, in one case as "an arbitrary initial guess" [6]. <!-- src: Yeh 2023 Methods (ligand-binding energy, protein-ligand hydrogen bonds, shape complementarity, contact molecular surface); Kim 2026 SI (Rosetta ddG, contact molecular surface, hydrogen bonds; AF2 pLDDT >= 72.5, Calpha RMSD <= 1.75 A; Chai-1 ipTM >= 0.7, pTM >= 0.875, PAE <= 6; weights "an arbitrary initial guess"); Listov 2025 Methods (fuzzy-logic objective: energy density, energy rank, active-site vdW, catalytic base vdW, ligand solvation, theozyme geometry); Braun 2026 (ranked predominantly by the sidechain RMSD of the catalytic tetrad); Butcher 2025 SI 4.1.1 (AF3 ensembles; motif RMSD < 1.25 then 1.0 A, pTM > 0.7 then 0.8, catalytic distances <= 3.5-4.0 A, pLDDT >= 90 targets, minimum chain-pair PAE < 5 A); Anishchenko 2025 and Lauko 2025 (PLACER ensembles, pRMSD) -->

Whether any of these metrics responds to catalysis is not known. A campaign judges its filter by its own hit rate, which also reflects every other change made between rounds. For the final selection, the designers of the metallohydrolases combined many metrics instead of applying cut-offs "due to the lack of known standalone predictive metrics for metallohydrolase activity" [6]. The authors of Riff-Diff report a "negligible correlation between predicted enzyme rankings and actual activity in this and previous studies" [11]. Systematic evaluations exist for neighbouring problems: filters for generated enzyme sequences [16], interface metrics for protein binders [17], predictor confidence for monomer designs [18, 19] and, in 2010, quantum-mechanical and molecular-dynamics scoring of the first Kemp-eliminase designs [20]. To our knowledge, none has asked whether the fast metrics that filter structure-based enzyme designs respond to catalysis. <!-- src: Kim 2026 SI "Filtering and analysis after PLACER" (verbatim); Braun 2026 Discussion (verbatim). Johnson 2025 abstract (20 metrics, over 500 generated malate dehydrogenase and copper superoxide dismutase sequences, success +50-150%; metrics describe sequences and apo predicted structures); Overath 2025 abstract (3,766 binders, 15 targets, over 200 features); Garcia 2026 abstract (614 monomers); Korbeld 2026 abstract (refolding filter); Kiss 2010 abstract (2008 Kemp-elimination designs, QM, QM/MM, MD). Background only, not cited: the Riff-Diff peer-review file, where the authors note that with 35 designs a correlation analysis of many computational metrics against activity has limited value -->

Here we test a panel of 33 metrics that can be computed from a design model or a co-folded prediction (Methods 2.1), and ask whether they respond to catalysis or to something simpler, such as how close a change is to the active site. We designed four tests. Two ask whether a metric can tell an active enzyme from an inactive one (*activity discrimination test*; 21 natural zymogen–mature pairs and 192 metallohydrolase designs, 16 of them active) and the cognate substrate from a wrong one (*substrate discrimination test*; 55 natural enzymes). A third asks whether a metric orders enzymes by their measured activity (*activity ranking test*; 432 variants of the β-glucosidase BglB and the 16 active designs). In the fourth we damage the catalytic residues of natural enzymes in the computer and ask whether a metric registers this more than the same damage at a matched non-catalytic site (*detection ability test*). Each test compares the metrics with trivial baselines, such as the distance to the catalytic residues.

A different metric led each test. Intra-residue repulsion of the catalytic residues led activity discrimination, but not beyond chance on the natural pairs (AUROC 0.61, against a chance threshold of 0.68 for the best of 39 items). On the designs the tyrosine fraction, which knows nothing about the active site, came close (0.75 against 0.80). ipTM led substrate discrimination (0.70). The range of the catalytic pKa ranked the BglB variants best (Spearman ρ = 0.48), but the distance from the mutated residue to the catalytic residues does almost as well (0.46) and no metric beat it. The per-chain pTM minimum responded most to catalytic damage (R = 0.75; 0.5 means no preference for the catalytic site) and fell to 0.59 when the control was matched on distance to the ligand. In three of the four tests, then, the best metric is matched by a simple reference or loses its advantage under a stricter control (Results 3.1 to 3.4). <!-- src: tables/public/main/T5_dead_vs_active.csv (intra-residue repulsion 0.61, best-of-39 95th percentile 0.68); T6_plated_designs_auroc.csv (0.80, tyrosine fraction 0.75); T7_substrate_swap.csv (ipTM mean 0.70); T8_bglb_variants.csv (pKa range 0.48, distance baseline 0.46, beats-baseline column all no); T10_specificity_catalytic_lesion.csv (per-chain pTM minimum 0.75, distance-matched 0.59). Not in the text: polar contacts lead the 16 active designs (T9, rho 0.67, descriptive); structure-space pKa range 0.68 in the lesion test -->

---

<!-- refs:start -->
## References for Section 1

*Reference numbers are local to this section.*

[1] Watson, J. L., Juergens, D., Bennett, N. R. et al. De novo design of protein structure and function with RFdiffusion. Nature 620, 1089–1100 (2023). doi:10.1038/s41586-023-06415-8 <!-- bib: watson2023 -->

[2] Ahern, W., Yim, J., Tischer, D. et al. Atom-level enzyme active site scaffolding using RFdiffusion2. Nature Methods 23, 96–105 (2026). doi:10.1038/s41592-025-02975-x <!-- bib: ahern2026 -->

[3] Butcher, J., Krishna, R., Mitra, R. et al. De novo Design of All-atom Biomolecular Interactions with RFdiffusion3. bioRxiv (2025). doi:10.1101/2025.09.18.676967 <!-- bib: butcher2025 -->

[4] Dauparas, J., Anishchenko, I., Bennett, N. et al. Robust deep learning-based protein sequence design using ProteinMPNN. Science 378, 49–56 (2022). doi:10.1126/science.add2187 <!-- bib: dauparas2022 -->

[5] Dauparas, J., Lee, G. R., Pecoraro, R. et al. Atomic context-conditioned protein sequence design using LigandMPNN. Nature Methods 22, 717–723 (2025). doi:10.1038/s41592-025-02626-1 <!-- bib: dauparas2025 -->

[6] Kim, D., Woodbury, S. M., Ahern, W. et al. Computational design of metallohydrolases. Nature 649, 246–253 (2026). doi:10.1038/s41586-025-09746-w <!-- bib: kim2026 -->

[7] Listov, D., Vos, E., Hoffka, G. et al. Complete computational design of high-efficiency Kemp elimination enzymes. Nature 643, 1421–1427 (2025). doi:10.1038/s41586-025-09136-2 <!-- bib: listov2025 -->

[8] Richter, F., Leaver-Fay, A., Khare, S. D., Bjelic, S., Baker, D. De novo enzyme design using Rosetta3. PLOS ONE 6, e19230 (2011). doi:10.1371/journal.pone.0019230 <!-- bib: richter2011 -->

[9] Lauko, A., Pellock, S. J., Sumida, K. H. et al. Computational design of serine hydrolases. Science 388, eadu2454 (2025). doi:10.1126/science.adu2454 <!-- bib: lauko2025 -->

[10] Yeh, A. H., Norn, C., Kipnis, Y. et al. De novo design of luciferases using deep learning. Nature 614, 774–780 (2023). doi:10.1038/s41586-023-05696-3 <!-- bib: yeh2023 -->

[11] Braun, M., Tripp, A., Chakatok, M. et al. Computational enzyme design by catalytic motif scaffolding. Nature 649, 237–245 (2026). doi:10.1038/s41586-025-09747-9 <!-- bib: braun2026 -->

[12] Jumper, J., Evans, R., Pritzel, A. et al. Highly accurate protein structure prediction with AlphaFold. Nature 596, 583–589 (2021). doi:10.1038/s41586-021-03819-2 <!-- bib: jumper2021 -->

[13] Abramson, J., Adler, J., Dunger, J. et al. Accurate structure prediction of biomolecular interactions with AlphaFold 3. Nature 630, 493–500 (2024). doi:10.1038/s41586-024-07487-w <!-- bib: abramson2024 -->

[14] Chai Discovery, Boitreaud, J., Dent, J. et al. Chai-1: Decoding the molecular interactions of life. bioRxiv (2024). doi:10.1101/2024.10.10.615955 <!-- bib: chai2024 -->

[15] Anishchenko, I., Kipnis, Y., Kalvet, I. et al. Modeling protein-small molecule conformational ensembles with PLACER. Proc. Natl. Acad. Sci. U.S.A. 122, e2427161122 (2025). doi:10.1073/pnas.2427161122 <!-- bib: anishchenko2025 -->

[16] Johnson, S. R., Fu, X., Viknander, S. et al. Computational scoring and experimental evaluation of enzymes generated by neural networks. Nature Biotechnology 43, 396–405 (2025). doi:10.1038/s41587-024-02214-2 <!-- bib: johnson2025 -->

[17] Overath, M. D., Rygaard, A. S. H., Jacobsen, C. P. et al. Predicting Experimental Success in De Novo Binder Design: A Meta-Analysis of 3,766 Experimentally Characterised Binders. bioRxiv (2025). doi:10.1101/2025.08.14.670059 <!-- bib: overath2025 -->

[18] Garcia, M., Dixit, S. M., Rocklin, G. J. Evaluating zero-shot prediction of monomeric protein design success by AlphaFold, ESMFold, and ProteinMPNN. Protein Sci. 35, e70453 (2026). doi:10.1002/pro.70453 <!-- bib: garcia2026 -->

[19] Korbeld, K. T., Viliuga, V., Fürst, M. J. L. J. Limitations of the refolding pipeline for de novo protein design. Protein Sci. 35, e70613 (2026). doi:10.1002/pro.70613 <!-- bib: korbeld2026 -->

[20] Kiss, G., Röthlisberger, D., Baker, D., Houk, K. N. Evaluation and ranking of enzyme designs. Protein Sci. 19, 1760–1773 (2010). doi:10.1002/pro.462 <!-- bib: kiss2010 -->

<!-- refs:end -->
