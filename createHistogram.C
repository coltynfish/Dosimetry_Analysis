#include "TH2F.h"
#include "TCanvas.h"
#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>

void createHistogram(const std::string& filename)
{
  gROOT->Reset();

gStyle->SetOptStat(11); //   ksiourmen , kurtosis & error (2), skewness &error(2), integral, overflows,
                        //    underflows, rms & error (2), mean & error (2), entries, title  pg 72
                        //    erase leading zeros

gStyle->SetOptFit(100); // pcev probability, chi-sqr/n-degrees, errors, values of parameters pg 129

gStyle->SetPalette(55);

gStyle->SetStatH(0.175);
gStyle->SetStatW(0.175);
gStyle->SetStatY(.9);
gStyle->SetStatX(.9);
gStyle->SetPadGridX(0);
gStyle->SetPadGridY(0);
gStyle->SetStatTextColor(1);
// gStyle->SetTitleX(0.1f);
// gStyle->SetTitleW(0.8f);
// gStyle->SetTitleY(0.96f);
// gStyle->SetTitleBorderSize(0);
gStyle->SetStatStyle(0);
gStyle->SetTitleStyle(0);
gStyle->SetMarkerColor(kWhite);

TGaxis::SetMaxDigits(3);

    // Open the text file
    std::ifstream inputFile(filename);
    if (!inputFile.is_open()) {
        std::cerr << "Error opening file: " << filename << std::endl;
        return;
    }

    // Read the positions from the file into a vector
    std::vector<std::vector<Double_t>> positions;
    std::string line;
    while (std::getline(inputFile, line)) {
        std::vector<Double_t> row;
        std::stringstream ss(line);
        Double_t value;
        while (ss >> value) {
            row.push_back(value);
        }
        positions.push_back(row);
    }

    // Close the file
    inputFile.close();

    // Create a 2D histogram
    Int_t numRows = positions.size();
    Int_t numCols = positions[0].size();
    TH2F* histogram = new TH2F("histogram", "2D Histogram", numCols, 0, numCols, numRows, 0, numRows);

    // Fill the histogram with data and set the bin contents at specific positions
    for (Int_t i = 0; i < numRows; ++i) {
        for (Int_t j = 0; j < numCols; ++j) {
            histogram->SetBinContent(j+1, numRows-i, positions[i][j]);

            // Set bin positions for placing values
            TString binLabel = Form("%.0f", positions[i][j]);
            histogram->GetXaxis()->SetBinLabel(j+1, binLabel);
            histogram->GetYaxis()->SetBinLabel(numRows-i, binLabel); // Set Y-axis labels in reverse order
        }
    }

    // Visualize the histogram
    TCanvas* canvas = new TCanvas("canvas", "Canvas Title", 800, 600);
    histogram->Draw("colz text");
    canvas->SetTitle("New Canvas Title");
    canvas->SaveAs("histogram.png");
}

int main()
{
    std::string filename = "E1_Positions.txt";
    createHistogram(filename);
    return 0;
}
