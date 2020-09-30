package ar.edu.itba.ss.mars;

import ar.edu.itba.ss.Integrator;
import ar.edu.itba.ss.oscillator.OscillatorParticle;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class MarsSimulation {

    private final MarsConfiguration configuration;
    private double time = 0;


    public MarsSimulation(MarsConfiguration configuration) {
        this.configuration = configuration;
    }


    public void run() {

        try {
            Files.deleteIfExists(Paths.get(getOutputFileName()));
        } catch (IOException e) {
            System.out.println("Unable to delete previously existing dynamic config");
        }

        // Initialize Particles
        // First doing this for just sun and earth
        List<Particle> particles = new ArrayList<>(2);

        Particle earth = new Particle(
                ParticleNames.EARTH,
                Constants.EarthConstants.STARTX,
                Constants.EarthConstants.STARTY,
                Constants.EarthConstants.STARTVX,
                Constants.EarthConstants.STARTVY,
                Constants.EarthConstants.MASS,
                Constants.EarthConstants.RADIUS,
                Constants.EarthConstants.VISUALIZATION_RADIUS,
                0,1,0);
        Particle sun = new Particle(ParticleNames.SUN, 0,0,0,0,
                Constants.SunConstants.MASS, Constants.SunConstants.RADIUS, Constants.SunConstants.VISUALIZATION_RADIUS,1, 1, 0);

        particles.add(earth);
        particles.add(sun);

        int iteration = 0;
        save(particles);
        while(time < configuration.getCutoffTime()) {
            for (Particle p : particles) {
                p.applyIntegrator(configuration.getIntegrator(), configuration.getDeltaT(), particles);
            }


            time += configuration.getDeltaT();
            iteration++;

            if (iteration % configuration.getSaveFrequency() == 0) {
                save(particles);
            }
        }
    }

    private String getOutputFileName() {
        String outFolder = configuration.getOutFolder();
        if (outFolder.charAt(outFolder.length() - 1) != '/') {
            outFolder = outFolder + "/";
        }
        return String.format("%s%s_dynamic.xyz", outFolder, configuration.getName());
    }


    public void save(List<Particle> particles) {
        try (FileWriter fw = new FileWriter(getOutputFileName(), true);) {

            // Format: x y VX VY radio R G B
            String particleFormat = "%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n";
            PrintWriter pw = new PrintWriter(fw);

            // If we want to add extra data, they should go here between the \n as to not affect the ovito output
            pw.printf(Locale.US, "%d\n\n", particles.size());

            for (Particle p : particles) {
                pw.printf(Locale.US, particleFormat,
                        p.getPosition().getX(),
                        p.getPosition().getY(),
                        p.getSpeed().getX(),
                        p.getSpeed().getY(),
                        p.getVisualizationRadius(),
                        p.getR(),
                        p.getG(),
                        p.getB());
            }

        } catch (IOException ex) {
            System.out.println("Unable to save, reason: " + ex.getMessage());
        }
    }
}