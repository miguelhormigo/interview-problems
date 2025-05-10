-- Create Machines table
CREATE TABLE machines (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

-- Create Simulations table
CREATE TABLE simulations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('pending', 'running', 'finished')),
    machine_id INTEGER REFERENCES machines(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Convergence table
CREATE TABLE convergence_data (
    id SERIAL PRIMARY KEY,
    simulation_id INTEGER REFERENCES simulations(id),
    seconds INTEGER NOT NULL,
    loss FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert initial data into Machines table
INSERT INTO machines (name, description) VALUES
('Machine A', 'High performance machine A'),
('Machine B', 'High performance machine B');

-- Insert initial data into Simulations table
-- INSERT INTO simulations (name, machine_id, status) VALUES 
-- ('Simulation 1', 1, 'finished'),
-- ('Simulation 2', 1, 'running'),
-- ('Simulation 3', 2, 'finished'),
-- ('Simulation 4', 2, 'pending'),
-- ('Simulation 5', 2, 'pending');

-- Insert initial data into Convergence table
-- INSERT INTO convergence_data (simulation_id, seconds, loss)
-- VALUES (1, 10, 0.8), (1, 20, 0.7), (1, 30, 0.65);