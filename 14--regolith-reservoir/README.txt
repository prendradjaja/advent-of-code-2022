Fun problem!

In a production codebase, I'd probably recommend using an implementation of
simulate_one_step() more like this. But I couldn't resist doing something
semi-clever...

    def simulate_one_step():
        def move_particle(pos):
            global grid, active_particle

            del grid[active_particle]
            active_particle = pos
            grid[active_particle] = 'o'

        global grid, active_particle

        assert grid.get(active_particle) == 'o'
        if is_empty(new_pos := addvec(active_particle, DOWN)):
            move_particle(new_pos)
        elif is_empty(new_pos := addvec(active_particle, DOWN_AND_LEFT)):
            move_particle(new_pos)
        elif is_empty(new_pos := addvec(active_particle, DOWN_AND_RIGHT)):
            move_particle(new_pos)
        else:
            assert is_empty(SOURCE)
            active_particle = SOURCE
            grid[active_particle] = 'o'

