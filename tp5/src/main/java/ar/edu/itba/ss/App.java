package ar.edu.itba.ss;

public class App {


    public static void main( String[] args ) {
        runMultipleSimulations();

        //runStandardSimulation();
    }

    public static void runStandardSimulation() {
        ConfigBuilder cb = new ConfigBuilder();
        Simulation sim = new Simulation(cb.createConfig());
        sim.run();
    }

    public static void runMultipleSimulations() {
        double[] safe_radius = {0.1, 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6};
        int simulations_qty = 10;

        for(int i=0; i< safe_radius.length; i++) {
            for(int j=0; j<simulations_qty; j++) {
                ConfigBuilder cb = new ConfigBuilder();
                cb.goalY(20); // fixed y for goal
                cb.startY(30); // fixed y for pedestrian
                cb.safePedestrianDistance(cb.pedestrianRadius + safe_radius[i]); // we update safe radius

                // filename
                StringBuilder sb = new StringBuilder();
                sb.append("sim_");
                sb.append(safe_radius[i]);
                sb.append("_");
                sb.append(j);
                cb.name(sb.toString());

                Simulation sim = new Simulation(cb.createConfig());
                sim.run();
            }
        }
    }
}
