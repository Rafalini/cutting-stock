import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def drawGraph(consumed_big_rolls, child_rolls, factoryRodSize, inputJsonDict):
    # TODO: to add support for multiple different parent rolls, update here
    xSize = factoryRodSize  # width of big roll
    ySize = 10 * len(consumed_big_rolls)  # one big roll will take 10 units vertical space

    # draw rectangle
    fig, ax = plt.subplots(1)
    plt.xlim(0, xSize)
    plt.ylim(0, ySize)
    plt.gca().set_aspect('equal', adjustable='box')

    # print coords
    coords = []
    colors = ['r', 'g', 'b', 'y', 'brown', 'violet', 'pink', 'gray', 'orange', 'b', 'y']
    colorDict = {}
    i = 0
    for quantity, width in child_rolls:
        colorDict[width] = colors[i % 11]
        i += 1

    # start plotting each big roll horizontly, from the bottom
    y1 = 0
    for i, big_roll in enumerate(consumed_big_rolls):
        '''
          big_roll = [leftover_width, [small_roll_1_1, small_roll_1_2, other_small_roll_2_1]]
        '''
        unused_width = big_roll[0]
        small_rolls = big_roll[1]

        x1 = 0
        x2 = 0
        y2 = y1 + 8  # the height of each big roll will be 8
        for j, small_roll in enumerate(small_rolls):
            x2 = x2 + small_roll
            width = abs(x1 - x2)
            height = abs(y1 - y2)
            # print(f"Rect#{idx}: {width}x{height}")
            # Create a Rectangle patch
            rect_shape = patches.Rectangle((x1, y1), width, height, facecolor=colorDict[small_roll],
                                           label=f'{small_roll}')
            ax.add_patch(rect_shape)  # Add the patch to the Axes
            x1 = x2  # x1 for next small roll in same big roll will be x2 of current roll

        # now that all small rolls have been plotted, check if a there is unused width in this big roll
        # set the unused width at the end as black colored rectangle
        if unused_width > 0:
            width = unused_width
            rect_shape = patches.Rectangle((x1, y1), width, height, facecolor='black', label='Unused')
            ax.add_patch(rect_shape)  # Add the patch to the Axes

        y1 += 10  # next big roll will be plotted on top of current, a roll height is 8, so 2 will be margin between rolls

    plt.savefig("output/"+inputJsonDict["fileName"]+".png")